from fastapi import FastAPI
import json
import prompts
import toml
import requests
import asyncio
import uuid


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
    scene_response = query_llm(scene_query, False)

    scene_data = json.loads(scene_response["text"][0])

    scenes[item[item["id"]]]["data"] = scene_data


app = FastAPI()


config = toml.load("config.toml")


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

    return storyboards


@app.get("/api/testing")
async def testing(testing: str = "default testing string"):
    return testing


@app.get("/api/scene/{scene_id}")
async def scene(scene_id: str):
    if scene_id not in scenes:
        return {"error": "Scene not found"}

    return scenes[scene_id]
