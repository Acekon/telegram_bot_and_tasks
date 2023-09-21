import fnmatch
import os
import random
import string

from PIL import Image, ImageDraw, ImageFont

full_path_img_dir = os.path.join(os.getcwd(), 'img\\')


def get_collage(mess_id):
    try:
        matching_files = []
        files_name = []
        for file_name in os.listdir(full_path_img_dir):
            if fnmatch.fnmatch(file_name, f'{mess_id}_*.png'):
                matching_files.append(os.path.abspath(full_path_img_dir + file_name))
                files_name.append(file_name)
        if matching_files:
            collage_path = create_image_collage(matching_files)
            return collage_path
    except FileNotFoundError:
        return f'Error please create {full_path_img_dir} dir'


def remove_collage(collage_path):
    if os.path.isfile(collage_path):
        os.remove(collage_path)


def create_image_collage(image_paths):
    random_prefix_file = ''.join(random.choice(string.ascii_letters) for i in range(6))
    output_path = f'{full_path_img_dir}collage_{random_prefix_file}.png'
    image_size = (200, 200)
    collage_size = (image_size[0] * len(image_paths), image_size[1])
    collage = Image.new('RGB', collage_size)
    for i, image_path in enumerate(image_paths):
        img_name = image_path.split('\\')[-1]
        image = Image.open(image_path)
        image = image.resize(image_size)
        im = ImageDraw.Draw(image)
        im.text((15, 170), f"{img_name}", fill=(255, 0, 0), font=ImageFont.truetype("arial.ttf", 22))
        collage.paste(image, (i * image_size[0], 0))
    collage.save(output_path)
    return output_path
