import json
import os
from moviepy.editor import *
from elevenlabs import generate, play, save, set_api_key
from codegen import generate_video_from_code

# Set your ElevenLabs API key
set_api_key("2bfa342d70b0f2c6e2221ba7bff79bf5")

# Assuming the JSON data is stored in a variable named 'scenes'
scenes = {
    "99e5afbf-a517-4ba0-951a-51e507b86901": {
        "title": "Vector Introduction",
        "description": "Introduce a vector with an arrow and label it as 'v' with components (x, y).",
        "id": "99e5afbf-a517-4ba0-951a-51e507b86901",
        "data": {
            "narration": "Today, let's talk about vectors. A vector is a mathematical object that has both a magnitude and a direction. We can represent a vector using an arrow, just like this one here.",
            "animation-description": "A horizontal number line is displayed at the center of the screen, ranging from -10 to 10 with ticks every 0.2. A red arrow is labeled 'v' with components (x, y) is drawn, pointing from 0 to +5. The arrow then shrinks until it points to +2.",
            "free-response-question": "Describe what a vector is and its two main properties.",
            "free-response-answer": "A vector is a mathematical object that has both a magnitude and a direction. It can be represented by an arrow, where the length of the arrow represents the magnitude and the direction in which the arrow is pointing represents the direction.",
            "multiple-choice-question": "What does a vector represent?",
            "multiple-choice-choices": [
                "A magnitude with no direction",
                "A direction with no magnitude",
                "Both a magnitude and a direction",
                "Neither a magnitude nor a direction"
            ],
            "code": "from manim import *\nimport numpy as np\n\nclass VectorIntroduction(Scene):\n    def construct(self):\n        number_line = NumberLine(x_range=[-10, 10, 0.2], length=10, include_numbers=True)\n        vector = Arrow(start=ORIGIN, end=[2, 0, 0], buff=0).set_color(RED)\n        vector_label = MathTex('v', font_size=24).next_to(vector, UP, buff=0.1)\n\n        self.play(Create(number_line))\n        self.play(GrowArrow(vector), Write(vector_label))\n        self.wait(1)\n        self.play(vector.animate.scale(0.4, about_point=ORIGIN))\n        self.wait(1)"
        }
    },
    "71526399-84a9-4472-b993-3c61fe4b21a5": {
        "title": "Matrix Introduction",
        "description": "Introduce a 2x2 matrix with each element labeled. Mention that this matrix will be used to multiply the vector.",
        "id": "71526399-84a9-4472-b993-3c61fe4b21a5",
        "data": {
            "narration": "Let's introduce a 2x2 matrix, where each element is labeled. We'll use this matrix to multiply a vector.",
            "animation-description": "Show a 2x2 matrix on the screen with each element labeled. The matrix should be centered horizontally and vertically on the screen. The size of the matrix should be legible, with a thin black border. The individual elements should be slightly spaced apart from each other.",
            "free-response-question": "Describe the process of matrix multiplication with a vector.",
            "free-response-answer": "Matrix multiplication with a vector involves multiplying each row of the matrix by the vector, resulting in a new vector. This is done by multiplying the corresponding elements in the row and vector, then summing the results to get the resulting vector element.",
            "multiple-choice-question": "What is the result of multiplying a 2x2 matrix by a 2D vector?",
            "multiple-choice-choices": [
                "A new 2D vector with the same number of elements as the original vector.",
                "A new 2D vector with twice the number of elements as the original vector.",
                "A new 2x2 matrix.",
                "A new 3D vector."
            ],
            "code": "from manim import *\nimport numpy as np\n\nclass MatrixIntroduction(Scene):\n    def construct(self):\n        matrix = Matrix([[Symbol('a'), Symbol('b')], [Symbol('c'), Symbol('d')]], v_buff=0.5, h_buff=0.5).set_stroke(width=0.5)\n        matrix_label = MathTex('A = ', font_size=24).next_to(matrix, LEFT)\n\n        self.play(Write(matrix_label), Write(matrix))\n        self.wait(1)"
        }
    },
    "53436c4e-5fb7-4b5d-8cb7-c8726a5e34df": {
        "title": "Vector-Matrix Multiplication",
        "description": "Align the vector with the first column of the matrix, then multiply each element of the vector with the corresponding element in the first column, summing the results to get the first element of the resulting vector.",
        "id": "53436c4e-5fb7-4b5d-8cb7-c8726a5e34df",
        "data": {
            "narration": "To multiply a matrix by a vector, we align the vector with the first column of the matrix, then multiply each element of the vector with the corresponding element in the first column, summing the results to get the first element of the resulting vector.",
            "animation-description": "A 2D matrix with dimensions 2x3 is displayed on the left side of the screen. A number line is centered vertically on the right side of the screen, ranging from -10 to 10 with ticks for every 0.2. A blue arrow is positioned above the number line, initially pointing from 0 to +5. The arrow then shrinks until it points to +2.",
            "free-response-question": "Describe the process of multiplying a matrix and a vector.",
            "free-response-answer": "To multiply a matrix and a vector, you align the vector with the first column of the matrix, then multiply each element of the vector with the corresponding element in the first column, summing the results to get the first element of the resulting vector. This process is repeated for each column in the matrix, resulting in a new vector.",
            "multiple-choice-question": "What is the first step in multiplying a matrix and a vector?",
            "multiple-choice-choices": [
                "Align the vector with the first column of the matrix",
                "Multiply each element of the vector with the corresponding element in the first column and summing the results",
                "Repeat the process for each column in the matrix",
                "All of the above"
            ],
            "code": "from manim import *\nimport numpy as np\n\nclass VectorMatrixMultiplication(Scene):\n    def construct(self):\n        matrix = Matrix([[Symbol('a'), Symbol('b')], [Symbol('c'), Symbol('d')]], v_buff=0.5, h_buff=0.5)\n        vector = Arrow(start=ORIGIN, end=[2, 0, 0], buff=0).set_color(BLUE)\n        vector_label = MathTex('(x, y)', font_size=24).next_to(vector, UP, buff=0.1)\n\n        self.play(Write(matrix))\n        self.play(GrowArrow(vector), Write(vector_label))\n        self.wait(1)\n        # Show the multiplication process visually (simplified for brevity)"
        }
    },
    "3b666767-0d93-4c98-ac76-f9b45076bbf7": {
        "title": "Resulting Vector",
        "description": "Repeat the previous step for the second column of the matrix, and show the resulting vector as the product of the vector-matrix multiplication.",
        "id": "3b666767-0d93-4c98-ac76-f9b45076bbf7",
        "data": {
            "narration": "Now let's take a look at what happens when we multiply a vector by a matrix. We'll start with the first column of the matrix.",
            "animation-description": "Show a 2x2 matrix with entries -3, 2, 5, 1. Highlight the first column of the matrix. Show a vector <1, 2> on the left side of the screen, above the matrix. Animate the vector being multiplied by the first column of the matrix, with the resulting vector <-3*1 + 2*2, 5*1 + 1*2> = <1, 6> displayed on the right side of the screen.",
            "free-response-question": "What is the result of multiplying a vector by a matrix?",
            "free-response-answer": "When multiplying a vector by a matrix, each element in the vector is multiplied by the corresponding elements in the matrix, and the resulting values are added together to give the resulting vector.",
            "multiple-choice-question": "What is the resulting vector of multiplying the vector <1, 2> by the matrix [[-3, 2], [5, 1]]?",
            "multiple-choice-choices": [
                "<1, 6>",
                "<6, 1>",
                "<-3, 5>",
                "<-6, -1>"
            ],
            "code": "from manim import *\nimport numpy as np\n\nclass ResultingVector(Scene):\n    def construct(self):\n        matrix = Matrix([[-3, 2], [5, 1]], v_buff=0.5, h_buff=0.5)\n        vector = MathTex('<1, 2>', font_size=24).to_edge(LEFT)\n        result_vector = MathTex('<1, 6>', font_size=24).to_edge(RIGHT)\n\n        self.play(Write(matrix), Write(vector))\n        self.wait(1)\n        self.play(Transform(vector, result_vector))\n        self.wait(1)"
        }
    },
    "509e73fa-69d1-422d-ba65-6a544da6f4ba": {
        "title": "Numerical Example",
        "description": "Perform the vector-matrix multiplication numerically, showing each step and the final calculation.",
        "id": "509e73fa-69d1-422d-ba65-6a544da6f4ba",
        "data": {
            "narration": "Let's perform a vector-matrix multiplication. We'll do it step by step.",
            "animation-description": "A number line is displayed centered vertically on the screen, ranging from -10 to 10 with ticks every 0.2. A blue arrow points from 0 to +5 above the number line. The arrow gradually shrinks until it points to +2.",
            "free-response-question": "Now that you've seen an example of vector-matrix multiplication, try it out with a different vector and matrix. Show your work.",
            "free-response-answer": "The correct answer will vary depending on the specific vector and matrix used.",
            "multiple-choice-question": "What is the resulting vector when performing the vector-matrix multiplication?",
            "multiple-choice-choices": [
                "(-2, 10, 1)",
                "(2, -10, 1)",
                "(-2, -10, 1)",
                "(2, 10, -1)"
            ],
            "code": "from manim import *\nimport numpy as np\n\nclass NumericalExample(Scene):\n    def construct(self):\n        # Assuming specific numerical example for brevity\n        matrix = Matrix([[1, 2], [3, 4]], v_buff=0.5, h_buff=0.5)\n        vector = MathTex('<x, y>', font_size=24).to_edge(LEFT)\n        result = MathTex('<result>', font_size=24).to_edge(RIGHT)\n\n        self.play(Write(matrix), Write(vector))\n        self.wait(1)\n        # Show numerical multiplication process (simplified)\n        self.play(Transform(vector, result))\n        self.wait(1)"
        }
    },
    "ea961601-6818-4e16-b45f-6772da1f381b": {
        "title": "Practical Example",
        "description": "Provide a real-world example of vector-matrix multiplication, such as transforming a vector in 2D space using a transformation matrix.",
        "id": "ea961601-6818-4e16-b45f-6772da1f381b",
        "data": {
            "narration": "Imagine you're a painter, and you want to move a certain distance along your 2D canvas. Let's say you want to move 3 units to the right and 4 units up. In vector notation, this can be represented as the vector (3, 4). Now, let's say you want to rotate this vector by 90 degrees clockwise. To do this, you'll need to use a transformation matrix.",
            "animation-description": "Start with a 2D plane and a vector pointing from the origin (0,0) to the point (3,4). Show a circle around the origin to indicate rotation. Then, display a transformation matrix with the values -1, 0, and 0, 1. Apply the transformation matrix to the vector, resulting in a new vector pointing from the origin to the point (-4, 3).",
            "free-response-question": "How would the vector (3, 4) change if it were rotated 180 degrees clockwise instead of 90 degrees?",
            "free-response-answer": "The vector (3, 4) would be transformed to the point (-3, -4).",
            "multiple-choice-question": "What is the result of rotating the vector (3, 4) 90 degrees clockwise?",
            "multiple-choice-choices": [
                "(-4, 3)",
                "(4, -3)",
                "(3, 4)",
                "(-3, 4)"
            ],
            "code": "from manim import *\nimport numpy as np\n\nclass PracticalExample(Scene):\n    def construct(self):\n        plane = NumberPlane(x_range=[-5, 5], y_range=[-5, 5])\n        vector = Arrow(start=ORIGIN, end=[3, 4, 0], buff=0)\n        matrix = Matrix([[-1, 0], [0, 1]], v_buff=0.5, h_buff=0.5)\n        transformed_vector = Arrow(start=ORIGIN, end=[-4, 3, 0], buff=0)\n\n        self.play(Create(plane))\n        self.play(GrowArrow(vector))\n        self.wait(1)\n        self.play(Transform(vector, transformed_vector))\n        self.wait(1)"
        }
    }
}


#print(scenes.items())
for scene_id, scene_details in scenes.items():
    narration_text = scene_details["data"]["narration"]
    mp3_filename = scene_id + '.mp3'
    
    # Check if audio file already exists to avoid re-generating it
    if not os.path.exists(mp3_filename):
        # Generate and save audio from narration text
        audio = generate(
            text=narration_text,
            voice="Charlie",
            model="eleven_multilingual_v1"
        )
        save(audio, mp3_filename)
    
    # Here you should execute the code from scene_details["code"] to generate a video clip
    # This part is highly dependent on your setup and the specifics of the manim code provided
    # For the sake of example, let's assume you have a function that handles this:
    mp4_filename = generate_video_from_code(scene_details["data"]["code"], "output")  # This is a placeholder function
    print("MP4" + mp4_filename)
    # Combine audio and video if both files exist
    if os.path.exists(mp4_filename) and os.path.exists(mp3_filename):
        videoclip = VideoFileClip(mp4_filename)
        audioclip = AudioFileClip(mp3_filename)
        videoclip = videoclip.set_audio(audioclip)
        videoclip.write_videofile(f"final_{scene_id}.mp4")
