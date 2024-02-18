import subprocess
import os
import textwrap
import re
import time

def generate_video_from_code(code_str, output_filename):
    """
    Executes Manim code to generate a video.
    
    :param code_str: A string containing the Python code to execute.
    :param output_filename: The name of the output video file.
    :return: The path to the generated video file or None if an error occurs.
    """
    # Dedent and strip the code string to ensure it's properly formatted
    code_str = textwrap.dedent(code_str).strip()
    print(code_str)
    # Attempt to extract the scene class name using regex
    match = re.search(r"class (\w+)\(Scene\):", code_str)
    if not match:
        print("No scene class found in the provided code string.")
        return None
    scene_class_name = match.group(1)
    print(match.group(1))

    # Define the path to a temporary Python file
    temp_script_path = f"temp_manim_script_{scene_class_name}.py"

    # Write the Manim code to the temporary file
    with open(temp_script_path, 'w') as temp_script:
        temp_script.write(code_str)
    print('Processing...')

    # Set a unique output directory based on the current time
    out_dir = f"media/{time.strftime('%Y-%m-%d-%H-%M-%S')}"

    # Make sure the output directory exists
    os.makedirs(out_dir, exist_ok=True)

    # Build the command to execute the Manim script
    command = [
        "manim",
        temp_script_path,
        scene_class_name,
        "-ql",  # Low quality for quicker generation, adjust as needed
        "--media_dir", out_dir
    ]

    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print("stdout:", result.stdout)
        print("stderr:", result.stderr)

        print("Video generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e.stderr}")
        return None
    #finally:
        # Clean up the temporary script file
        #os.remove(temp_script_path)

    # Construct the path to the generated video file
    video_path = os.path.join(out_dir, "videos", temp_script_path.replace('.py', ''), scene_class_name, "480p15", f"{scene_class_name}.mp4")
    print(f"Video saved to {video_path}")
    return video_path

# Example usage
# code_str = """
# from manim import *

# class VectorIntroduction(Scene):
#     def construct(self):
#         # Your scene content
# """
# output_filename = "VectorIntroduction"
# video_path = generate_video_from_code(code_str, output_filename)
# if video_path:
#     print(f"Video generated at: {video_path}")
