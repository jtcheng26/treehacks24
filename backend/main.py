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


loop = asyncio.get_event_loop()
loop.create_task(process_queue())


async def generate_scene(item):
    print("Generating scene: ", item["id"], item["title"])

    if item["id"] not in scenes:
        print("Creating new scene: ", item["id"])
        scenes[item["id"]] = {}
    # item has, key, title and description

    # Generate the scene information
    scene_query = prompts.SCENE_AGENT_PROMPT.format(item["description"])

    print(scene_query)

    scene_response = await async_query_llm(scene_query, False)

    print(scene_response)

    work = False

    while not work:
        try:
            print("Trying to parse JSON...")
            text = scene_response["text"][0]
            # remove everything before the first {
            text = text[text.index("{") :]
            # remove everything after the last }
            text = text[: text.rindex("}") + 1]
            print(text)
            scene_data = json.loads(text)
            work = True

        except json.JSONDecodeError as e:
            scene_query += (
                "\n\n"
                + scene_response["text"][0]
                + "\n\nTHIS IS NOT VALID JSON. PLEASE FIX IT. RETURN ONLY A VALID JSON FORMAT."
            )

            print("Invalid JSON")
            print(scene_query)
            scene_response = await async_query_llm(scene_query, False)

    scenes[item["id"]]["data"] = scene_data

    # Generate the animation code

    animation_query = prompts.ANIMATION_PROMPT.format(
        scene_data["narration"], scene_data["animation-description"]
    )

    print(animation_query)

    animation_response = await async_query_llm(animation_query, False)
    # todo: deal with fine tuning = true

    print(animation_response)

    animation_code = animation_response["text"][0]
    scenes[item["id"]]["code"] = animation_code

    # Generate the video
    await generate_video(item["id"])

    # Write the data to a file
    with open("scenes.json", "w") as f:
        json.dump(scenes, f, indent=4)


async def generate_video(item_id):
    print("Generating video: ", item_id)
    # Generate the video from the code

    with open(f"scene_{item_id}.py", "w") as f:
        f.write(scenes[item_id]["code"])

    # Run the manim command
    try:
        os.system(f"manim scene_{item_id}.py -o -lq scene_{item_id}.mp4")
    except Exception as e:
        print("Error: ", e)
    # todo: deal with what happens when it errors out

    # Do something with audio generation
    # todo:

    # todo splice togehter

    # todo: the guy's face


app = FastAPI()


config = toml.load("config.toml")


async def async_query_llm(prompt: str, is_code: bool = False):
    return query_llm(prompt, is_code)
    # model = "c" if is_code else "codellama"
    model = "mixtral"

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
        "temperature": 0.65,
        "top_p": 0.9,
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
            data = await response.json()
            return json.loads(data)


def query_llm(prompt: str, is_code: bool = False):
    # model = "mixtal" if is_code else "codellama"
    model = "mixtral"

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

    print(response)

    query_save = {
        "prompt": formatted_prompt,
        "response": response,
    }

    storyboard_query_save.append(query_save)

    # storyboards = json.loads(response["text"][0])["frames"]
    valid = False

    while not valid:
        try:
            print("Trying to parse JSON...")
            text = response["text"][0]
            # remove everything before the first {
            text = text[text.index("{") :]
            # remove everything after the last }
            text = text[: text.rindex("}") + 1]
            print(text)
            storyboards = json.loads(text)["frames"]
            valid = True
        except json.JSONDecodeError as e:
            formatted_prompt += (
                "\n\n"
                + response["text"][0]
                + "\n\nTHIS IS NOT VALID JSON. PLEASE FIX IT. RETURN ONLY A VALID JSON FORMAT."
            )
            print("Invalid JSON")
            print(formatted_prompt)
            response = query_llm(formatted_prompt, False)

    # storyboards = json.loads(response["text"][0])["frames"]

    for storyboard in storyboards:
        id = str(uuid.uuid4())
        scenes[id] = storyboard
        storyboard["id"] = id
        queue.put_nowait(storyboard)

    return storyboards


@app.get("/api/testing")
async def testing(testing: str = "default testing string"):
    print("running scene gen")

    return testing


@app.get("/api/scene/{scene_id}")
async def scene(scene_id: str):
    if scene_id not in scenes:
        return {"error": "Scene not found"}

    return scenes[scene_id]


@app.get("/api/video/{scene_id}")
async def video(scene_id: str):
    if scene_id not in scenes:
        return {"error": "Scene not found"}

    # check if the video exists
    if not os.path.exists(f"scene_{scene_id}.mp4"):
        return {"error": "Video not found"}

    return fastapi.responses.FileResponse(f"scene_{scene_id}.mp4")
