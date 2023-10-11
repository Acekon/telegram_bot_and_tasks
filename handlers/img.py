import fnmatch
import os
import random
import string

import requests
from PIL import Image, ImageDraw, ImageFont

full_path_img_dir = os.path.join(os.getcwd(), 'img\\')


def get_collage(mess_id, type_collage=None):
    try:
        matching_files = []
        files_name = []
        for file_name in os.listdir(full_path_img_dir):
            if fnmatch.fnmatch(file_name, f'{mess_id}_*.png'):
                matching_files.append(os.path.abspath(full_path_img_dir + file_name))
                files_name.append(file_name)
        if matching_files:
            if type_collage == 'vertical':
                collage_path = create_vertical_collage(matching_files)
                return collage_path
            collage_path = create_image_collage(matching_files)
            return collage_path
    except FileNotFoundError:
        return f'Error please create {full_path_img_dir} dir'


def remove_collage(collage_path):
    if os.path.isfile(collage_path):
        os.remove(collage_path)


def create_image_collage(image_paths):
    random_prefix_file = ''.join(random.choice(string.ascii_letters) for _ in range(6))
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


def create_vertical_collage(image_paths):
    width = 300
    random_prefix_file = ''.join(random.choice(string.ascii_letters) for _ in range(6))
    output_path = f'{full_path_img_dir}collage_{random_prefix_file}.png'
    image_size = (200, 200)
    collage_height = image_size[1] * len(image_paths)
    if len(image_paths) >= 5:
        width = len(image_paths) * 100
    collage_width = image_size[0] + width
    collage = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))
    images_name = []
    for i, image_path in enumerate(image_paths):
        img_name = image_path.split('\\')[-1]
        images_name.append(img_name)
        image = Image.open(image_path)
        image = image.resize(image_size)
        collage.paste(image, (0, i * image_size[1]))
        draw = ImageDraw.Draw(collage)
        text_x = image_size[0] + 10
        text_y = i * image_size[1] + image_size[1] // 2
        text_color = (0, 0, 0)
        font = ImageFont.truetype("arial.ttf", 20)
        draw.text((text_x, text_y), img_name, fill=text_color, font=font)
    collage.save(output_path)
    return output_path, images_name


def download_img(file_id, bot_token, mess_id):
    file_info = requests.get(f'https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}')
    file_path = file_info.json()['result']['file_path']
    response_img = requests.get(f'https://api.telegram.org/file/bot{bot_token}/{file_path}')
    random_prefix_file = ''.join(random.choice(string.ascii_letters) for _ in range(6))
    with open(f"img/{mess_id}_{random_prefix_file}.png", 'wb') as f:
        f.write(response_img.content)
    return f"File {mess_id}_{random_prefix_file}.png is uploads"


def remove_img(img_path, img_name=None):
    if img_name:
        os.remove(full_path_img_dir + img_name)
        return True
    if os.path.isfile(f'{img_path}'):
        os.remove(img_path)
        return True
    else:
        return f"File not found: ({img_path})"


def remove_all_img(mess_id):
    matching_files = []
    files_name = []
    for file_name in os.listdir(full_path_img_dir):
        if fnmatch.fnmatch(file_name, f'{mess_id}_*.png'):
            matching_files.append(os.path.abspath(full_path_img_dir + file_name))
            files_name.append(file_name)
    if matching_files:
        for img_path in matching_files:
            remove_img(img_path)
        return files_name
    else:
        return False


if __name__ == '__main__':
    # print(remove_img('E:\\Dev\\Project\\humor\\TG_task_and_bot_sender\\img\\2_3.png'))
    # remove_all_img('48')
    pass
