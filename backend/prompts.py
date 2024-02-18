STORYBOARD_PROMPT = """For an audience of a {}, generate a series of frames to explain {}  Each frame should be a single animation point, such as visualizing squaring number visually or adding a vector tip to tail. It should not take longer than 15 seconds.

For example, explaining a vector addition would be:
1. Frame showing 2 vectors from the origin explaining that these can be any arbitary vector
2. Moving the second vector to the tip of the first vector and draw a resulting vector
3. Showing vector addition numerically, adding each component numerically
4. Explain a simple practical example of vector addition, how 2 forces can combine togehter into a larger force.

Do not include a frame for a quiz. 

Each frame should come with a short description of what it will talk about. This is meant to be the storyboard for an animated video explaining this concept. 

Format the frames in the following json format:

{{ "frames": 
[
{{
"title": "xxxx",
"description": "xxxx"
}},
]
}}

Ensure that the json is valid.

The title should be short, limit of 5 words
The description should be a few sentences, enough for someone to understand what to do and how to animate and explain this frame.

Output only the json format of the frames. DO NOT INCUDE A PREABMBLE OR POSTAMBLE.
"""


SCENE_AGENT_PROMPT = """Given the following, generate a script and animation description in the style of 3Blue1Brown.

{}

The script will be read orally to the student. This should not take longer than 10-15 seconds.
The animation description should be descriptive of what should be shown on the screen along with relevant positional information. (ie. The number line should be centered vertically on the screen with a from a range of -10 to 10 with ticks for every 0.2, there is a blow arrow above the number line pointing from 0 to +5. The arrow will then shrink until it points to +2)

In addition, generate a 4 choice multiple choice question and a free response question that can be asked at the end of the video.

The corrent answer for the multiple choice should always be the first in the array. The answer for the free response should be a string.

Return the data in the following format:

{{
"narration" : "string",
"animation-description": "string",
"free-response-question": "string",
"free-response-answer": "string",
"multiple-choice-question": "string",
"multiple-choice-choices": ["answer - string", "wrong - string", "wrong - string", "wrong - string"],
}}
"""

ANIMATION_PROMPT = """
1. Given the scene description, write manim (CE) code for this scene in 3blue1brown style.
2. Make sure that the any LaTeX equations are rendered correctly.
3. Make sure that the font_size is small (< 25pt).
4. Make sure no manim objects have the same y coordinate to ensure no overlapping.
5. Make sure any text, diagrams or formulas fit fully on the screen. Make them smaller.
6. Text should be concise and to the point, no more than 10 words.
7. Make sure that the mathematics is consistent with the narration.
8. Make sure that all visualizations are coherent and has a mathematical basis.
9. Write the whole code in one chunk at every code generation stage.
11. You are allowed to import manim, import numpy as np.
12. Use default manim colors and styles.
13. DO NOT INCLUDE ANY OUTSIDE GRAPHICS OR IMAGES. ONLY USE MANIM.
14. Only include the manim code for the scene. DO NOT INCLUDE A PREABMBLE OR POSTAMBLE.

Narration: (given for additional context)
{}

Animation Description:
{}
"""
