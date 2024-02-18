from fastapi import FastAPI
import together
import json

together.api_key = "9fcd816a3e4499c7b604182d817edbf800dacf99e869d37fd1ce32f039350752"

app = FastAPI()

prompt = """[INST] For an audience of a {}, generate a series of frames to explain {}  Each frame should be a single animation point, such as visualizing squaring number visually or adding a vector tip to tail. It should not take longer than 15 seconds.

For example, explaining a vector addition would be:
1. Frame showing 2 vectors from the origin explaining that these can be any arbitary vector
2. Moving the second vector to the tip of the first vector and draw a resulting vector
3. Showing vector addition numerically, adding each component numerically
4. Explain a simple practical example of vector addition, how 2 forces can combine togehter into a larger force.

Do not include a frame for a quiz. 

Each frame should come with a short description of what it will talk about. This is meant to be the storyboard for an animated video explaining this concept. 

Format the frames in a json format: 

[
{{
"title": "xxxx",
"description": "xxxx"
}},
]

The title should be short, limit of 5 words
The description should be a few sentences, enough for someone to understand what to do and how to animate and explain this frame.

Output only the json format of the frames. DO NOT INCUDE A PREABMBLE OR POSTAMBLE. [/INST]
"""

MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"


@app.get("/")
async def root():
    return {"message": "Hello World"}


cached_storyboard = {}


@app.get("/api/init")
async def init(audience: str = "high school student", concept: str = "vector addition"):
    formatted = prompt.format(audience, concept)

    output = together.Complete.create(
        prompt=formatted,
        model=MODEL,
        max_tokens=2048,
        temperature=0.7,
        top_p=0.5,
        top_k=50,
        repetition_penalty=1.0,
        stop=["</s>", "[/INST]"],
    )

    data = json.loads(output["output"]["choices"][0]["text"])

    global cached_storyboard
    cached_storyboard = data

    return data
