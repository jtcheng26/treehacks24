import os
from fastapi import FastAPI
import json

import fastapi
import prompts
import toml
import requests
import asyncio
import uuid
import aiohttp

# Event loop for querying each scene

queue = asyncio.Queue()


async def process_queue():
    while True:
        item = await queue.get()
        await generate_scene(item)
        queue.task_done()


async def generate_scene(item):
    # item has, key, title and description

    # Generate the scene information
    scene_query = prompts.SCENE_AGENT_PROMPT.format(item["description"])
    scene_response = await query_llm(scene_query, False)

    scene_data = json.loads(scene_response["text"][0])

    scenes[item[item["id"]]]["data"] = scene_data

    animation_query = prompts.ANIMATION_PROMPT.format(
        scene_data["narration"], scene_data["animation-description"]
    )

    animation_response = await query_llm(animation_query, False)
    # todo: deal with fine tuning = true
    animation_code = animation_response["text"][0]
    scenes[item[item["id"]]]["code"] = animation_code

    # Generate the video
    generate_video(item["id"])


async def generate_video(item_id):
    # Generate the video from the code

    with open(f"scene_{item_id}.py", "w") as f:
        f.write(scenes[item_id]["code"])

    # Run the manim command
    os.system(f"manim scene_{item_id}.py -o -lq scene_{item_id}.mp4")
    # todo: deal with what happens when it errors out

    # Do something with audio generation
    # todo:

    # todo splice togehter

    # todo: the guy's face


app = FastAPI()


config = toml.load("config.toml")


async def async_query_llm(prompt: str, is_code: bool = False):
    model = "mixtal" if is_code else "codellama"

    payload_body = {
        "input_variables": {"prompt": prompt},
        # "prompt": prompt,
        "stream": False,
        "max_tokens": 8192,
        "n": 1,
        "best_of": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "repetition_penalty": 1,
        "temperature": 0.7,
        "top_p": 1,
        "top_k": -1,
        "min_p": 0,
        "use_beam_search": False,
        "length_penalty": 1,
        "early_stopping": False,
    }

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {config[f'{model}_auth_token']}",
        "Content-Type": "application/json",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            config[f"{model}_url"] + "/generate",
            headers=headers,
            json=payload_body,
        ) as response:
            return await json.loads(response.json())


def query_llm(prompt: str, is_code: bool = False):
    model = "mixtal" if is_code else "codellama"

    payload_body = {
        "input_variables": {"prompt": prompt},
        # "prompt": prompt,
        "stream": False,
        "max_tokens": 8192,
        "n": 1,
        "best_of": 1,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "repetition_penalty": 1,
        "temperature": 0.7,
        "top_p": 1,
        "top_k": -1,
        "min_p": 0,
        "use_beam_search": False,
        "length_penalty": 1,
        "early_stopping": False,
    }

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {config[f'{model}_auth_token']}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        config[f"{model}_url"] + "/generate",
        headers=headers,
        json=payload_body,
    )

    return json.loads(response.json())


@app.get("/")
async def root():
    return {"message": "Hello World"}


storyboard_query_save = []
scenes = {}


@app.get("/api/init/")
async def init(audience: str = "high school student", concept: str = "vector addition"):
    formatted_prompt = prompts.STORYBOARD_PROMPT.format(audience, concept)

    print(formatted_prompt)

    response = query_llm(formatted_prompt, False)

    query_save = {
        "prompt": formatted_prompt,
        "response": response,
    }

    storyboard_query_save.append(query_save)

    storyboards = json.loads(response["text"][0])

    for storyboard in storyboards:
        scenes[str(uuid.uuid4())] = storyboard
        storyboard["id"] = str(uuid.uuid4())
        queue.put_nowait(storyboard)

    return storyboards


@app.get("/api/testing")
async def testing(testing: str = "default testing string"):
    return testing


@app.get("/api/scene/{scene_id}")
async def scene(scene_id: str):
    if scene_id not in scenes:
        return {"error": "Scene not found"}

    return scenes[scene_id]


@app.get(f"/api/video/{scene_id}")
async def video(scene_id: str):
    if scene_id not in scenes:
        return {"error": "Scene not found"}

    # check if the video exists
    if not os.path.exists(f"scene_{scene_id}.mp4"):
        return {"error": "Video not found"}

    return fastapi.responses.FileResponse(f"scene_{scene_id}.mp4")
