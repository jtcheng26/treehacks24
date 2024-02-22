import os
import re
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

import json

import fastapi
import prompts
import toml
import requests
import asyncio
import uuid
import aiohttp

import pathlib
import textwrap

import subprocess

import time

from starlette.concurrency import run_in_threadpool

from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.editor import *






# Event loop for querying each scene

app = FastAPI()


config = toml.load("config.toml")

from elevenlabs import generate, play, save, set_api_key
set_api_key(config["elevenlabs_api_key"])


async def generate_scene(item, i=0, err=''):
    global scenes
    if i > 10:
        return
    print("Generating scene: ", item["id"], item["title"])

    if item["id"] not in scenes:
        print("Creating new scene: ", item["id"])
        scenes[item["id"]] = {}
    # item has, key, title and description

    # Generate the scene information
    scene_query = prompts.SCENE_AGENT_PROMPT.format(item["description"]) + (
        '' if not err else '\nThese were the errors from the last run please resolve them: ' + err)

    print(scene_query)

    scene_response = await run_in_threadpool(query_gpt, scene_query, False, True)

    print(scene_response)

    work = False

    while not work:
        try:
            print("Trying to parse JSON...")
            text = scene_response
            # remove everything before the first {
            text = text[text.index("{"):]
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
            scene_response = await run_in_threadpool(query_gpt, scene_query, False)

    scenes[item["id"]]["data"] = scene_data

    # Generate the animation code

    animation_query = prompts.ANIMATION_PROMPT.format(
        scene_data["narration"], scene_data["animation-description"]
    )

    print(animation_query)

    animation_response = await run_in_threadpool(query_gpt, animation_query, False, True)
    # todo: deal with fine tuning = true

    print(animation_response)

    animation_code = animation_response
    scenes[item["id"]]["code"] = animation_code

    # Generate the video
    await generate_video(item["id"], i)

    # Write the data to a file
    with open("scenes.json", "w") as f:
        json.dump(scenes, f, indent=4)


@app.get("/api/generate")
async def generate_video(item_id: str, i=0, err = ''):
    if i > 10:
        print("FAILED TEN TIMES")
        return
    print("Generating video: ", item_id)
    global scenes
    # scenes = json.load(open("scenes.json"))
    # Generate the video from the code

    def extract_code_blocks(input_string, pattern):
        matches = re.findall(pattern, input_string, re.DOTALL)

        return matches

    with open(f"scene_code/scene_{item_id}.py", "w") as f:
        uh = textwrap.dedent(scenes[item_id]["code"]).rstrip()
        res = extract_code_blocks(uh, r'```python(.*?)```')
        res2 = extract_code_blocks(uh, r'```(.*?)```')
        if len(res) and len(res[0]):
            res = textwrap.dedent(res[0]).rstrip()
            f.write(
                'from manim import *\nconfig.background_color = "#0F172A"\n' + res)
        elif len(res2) and len(res2[0]):
            res2 = textwrap.dedent(res2[0]).rstrip()
            f.write(
                'from manim import *\nconfig.background_color = "#0F172A"\n' + res2)
        else:
            f.write('from manim import *\nconfig.background_color = "#0F172A"\n' + uh)

    # Run the manim command
    try:
        # # log all output
        # cmd_output = os.system(f"manim scene_{item_id}.py -o -lq scene_{item_id}.mp4")

        # os.system(f"manim scene_{item_id}.py -o -lq scene_{item_id}.mp4")
        print("new")

        command = [
            "manim",
            f"scene_code/scene_{item_id}.py",
            "-ql",
            "-o",
            pathlib.Path(__file__).parent /
            "scene_code" / f"scene_{item_id}",
        ]

        async def run_command(command):

            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            return process.returncode, stdout.decode(), stderr.decode()
        exitcode, stdout, stderr = await run_command(command)
        narration_text = scenes[item_id]["data"]["narration"]
        audio_filename = f"scene_audio/scene_{item_id}.mp3"
        
        # Check if the audio file already exists to avoid regenerating it
        if not os.path.exists(audio_filename):
            print("Generating audio narration for: ", item_id)
            # Assuming you have a function `generate_audio` that encapsulates the audio generation logic
            audio = generate(
                text=narration_text,
                voice="Charlie",
                model="eleven_multilingual_v1"
            )
        # Assuming you have a function `save_audio` to save the generated audio
        save(audio, audio_filename)
        video_clip = VideoFileClip(f"scene_code/scene_{item_id}.mp4")
        audio_clip = AudioFileClip(audio_filename)
        final_clip = video_clip.set_audio(audio_clip)
    

        final_video_filename = f"scene_code/scene_{item_id}.mp4"
        final_clip.write_videofile(final_video_filename)
        print("EXITCODE", exitcode)
        print(stdout)
        print("STDERRRR", stderr)
        if (exitcode != 0):
            if stderr != '' or not os.path.exists(f"scene_code/scene_{item_id}.mp4"):
                print("NO FILE FOUND", item_id)
                await generate_scene(scenes[item_id], i + 1, stderr[-100:])

    except subprocess.CalledProcessError as e:
        print("Error: ", e)
        print(e.stderr)
        print("llll")

    # todo: deal with what happens when it errors out

    print("done")

    # Do something with audio generation
    # todo:

    # todo splice togehter

    # todo: the guy's face


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        verify=False,
    )

    return json.loads(response.json())


def query_gpt(prompt: str, temp=False, is_manim=False):
    # model = "mixtral" if is_code else "codellama"

    payload_body = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": "You are a 3blue1brown assistant. You are helping 3blue1brown to generate a scene for his next video. You are proficient in manim and very capable. DO NOT DOUBT YOURSELF." if is_manim else "You are an assistant to generate JSON code.",
            },
            {"role": "user", "content": prompt},
        ],
    }

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {config[f'openai_auth_token']}",
        "Content-Type": "application/json",
    }

    # print(headers)
    # print(payload_body)

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload_body,
    )
    res = response.json()
    print(res)
    if "choices" not in res:
        return ""

    return res["choices"][0]["message"]["content"]


@app.get("/")
async def root():
    return {"message": "Hello World"}


storyboard_query_save = []
scenes = {}


@app.get("/api/init/")
async def init(audience: str = "high school student", concept: str = "vector addition"):
    global scenes
    # with open('./scenes.json', 'r') as r:
    #     scene = json.load(r)  # d
    #     scenes = scene

    # time.sleep(0.5)  # d

    # return list(scene.values())  # d
    formatted_prompt = prompts.STORYBOARD_PROMPT.format(audience, concept)

    print(formatted_prompt)

    response = json.loads(await run_in_threadpool(query_gpt, formatted_prompt, False))

    print(response)

    query_save = {
        "prompt": formatted_prompt,
        "response": response,
    }

    storyboard_query_save.append(query_save)

    # storyboards = json.loads(response["text"][0])["frames"]
    # valid = True
    # text = extract_code_blocks(uh, r'```python(.*?)```')
    # res2 = extract_code_blocks(uh, r'```(.*?)```')
    # if len(res) and len(res[0]):
    #     res = textwrap.dedent(res[0]).rstrip()
    # with open('tempsdf', 'w') as w:
    #     w.write(response)

    # while not valid:
    #     try:
    #         print("Trying to parse JSON...")
    #         print(response.keys())
    #         text = response["text"][0]
    #         # remove everything before the first {
    #         text = text[text.index("{"):]
    #         # remove everything after the last }
    #         text = text[: text.rindex("}") + 1]
    #         print(text)
    #         storyboards = json.loads(text)["frames"]
    #         valid = True
    #     except json.JSONDecodeError as e:
    #         formatted_prompt += (
    #             "\n\n"
    #             + response["text"][0]
    #             + "\n\nTHIS IS NOT VALID JSON. PLEASE FIX IT. RETURN ONLY A VALID JSON FORMAT."
    #         )
    #         print("Invalid JSON")
    #         print(formatted_prompt)
    #         response = run_in_threadpool(query_gpt, formatted_prompt, False)

    storyboards = response["frames"]
    with open('uuids.txt', 'w') as w:
        w.write(json.dumps(storyboards))

    for storyboard in storyboards:
        id_s = str(uuid.uuid4())
        scenes[id_s] = storyboard
        storyboard["id"] = id_s
        asyncio.create_task(generate_scene(storyboard))

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
    # assert os.path.exists('scene_code/scene_9eb1415b-870e-4519-8beb-f2d01385ce6a.mp4')
    if not os.path.exists(f"scene_code/scene_{scene_id}.mp4"):
        return {"error": "Video not found"}

    return fastapi.responses.FileResponse(f"scene_code/scene_{scene_id}.mp4")


# check freeform text answers


@app.post("/api/text_answer")
async def check_answer(request: Request):
    data = await request.json()
    print(data)
    formatted_prompt = prompts.CHECK_ANSWER_PROMPT.format(
        data["answer"], data["question"]
    )

    print(formatted_prompt)

    # response = query_llm(formatted_prompt, False)

    response = await run_in_threadpool(query_gpt, formatted_prompt)
    # response = "YES"
    # print(response)

    return fastapi.responses.PlainTextResponse(response)
