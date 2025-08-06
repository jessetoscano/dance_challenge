from PIL import Image
import os

def extract_gif_frames(gif_path, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Open the GIF file
        with Image.open(gif_path) as im:
            for i in range(im.n_frames):
                im.seek(i)
                # Create a frame file name (e.g., frame_0001.png)
                frame_name = f"frame_{i:04d}.png"
                frame_path = os.path.join(output_dir, frame_name)
                im.save(frame_path)
            print(f"Successfully extracted {im.n_frames} frames to '{output_dir}' folder.")

    except FileNotFoundError:
        print(f"Error: The file '{gif_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# The name of your GIF file, updated with an underscore
gif_file = "space_galaxy.gif"
# The folder where the extracted frames will be saved
output_folder = "space_galaxy-frames"

extract_gif_frames(gif_file, output_folder)