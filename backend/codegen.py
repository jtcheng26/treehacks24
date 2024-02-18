import subprocess
import os
import textwrap

def generate_video_from_code(code_str, output_filename):
    """
    Executes Manim code to generate a video.
    
    :param code_str: A string containing the Python code to execute.
    :param output_filename: The name of the output video file.
    :return: The path to the generated video file.
    """
    # Define the path to a temporary Python file
    temp_script_path = 'temp_manim_script.py'
    code_str = textwrap.dedent(code_str).strip()

    # Write the Manim code to the temporary file
    with open(temp_script_path, 'w') as temp_script:
        temp_script.write(code_str)
    print('hey')
    # Define the command to execute the Manim script
    # Ensure you have Manim installed and the manim command is accessible
    execute_command = f"manim -pql {temp_script_path} {output_filename}"
    
    # Execute the command
    try:
        subprocess.run(execute_command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while generating the video: {e}")
        return None
    finally:
        # Optionally, clean up the temporary script file
        os.remove(temp_script_path)
    
    # Return the path to the generated video
    return output_filename + '.mp4'  # Adjust based on how Manim names output files
