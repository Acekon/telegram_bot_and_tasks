from PIL import Image
import os

# Specify the input directory and output directory

print('Enter full path to directory of images')
input_directory = input()
output_directory = f'{input_directory}_resized'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Loop through all files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
        # Open the image
        with Image.open(os.path.join(input_directory, filename)) as img:
            # Resize the image to 600x600
            img = img.resize((600, 600))

            # Save the resized image to the output directory
            output_path = os.path.join(output_directory, filename)
            print(f"Save{output_directory, filename}")
            img.save(output_path)
