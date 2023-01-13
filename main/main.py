import os
import pathlib
import subprocess

import cv2
from skimage.metrics import structural_similarity as ssim
from sklearn.metrics import mean_squared_error as mse

from image import Image


def give_list_frame_path(name_dir) -> [str]:
    res = []
    d = pathlib.Path(name_dir)
    for entry in d.iterdir():
        if entry.is_file():
            res.append(str(entry))
    return res


def predict(file_path: str, folder_path: str):
    tmp_simular = -1
    tmp_mse = float(10000)

    img = cv2.imread(file_path)
    height, width = img.shape[:2]

    first_image = Image(img, height, width)
    print(first_image.get_central_pixel())

    for image_name in give_list_frame_path(folder_path):
        ref = cv2.imread(image_name)
        second_image = Image(ref, height, width)

        if first_image.compare(second_image.get_central_pixel()):
            gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
            (simular, diff) = ssim(gray1, gray2, full=True)
            mse_cof = mse(gray1, gray2)

            if simular > tmp_simular:
                tmp_simular = simular
                tmp_mse = mse_cof
                print(image_name)
                print(simular)
                print(mse_cof)
    print(f'mse: {tmp_mse} \n simular: {tmp_simular}')


def compress_files_from_dir(dir_name: str):
    for image_name in give_list_frame_path(dir_name):
        compress_img(image_name)


def create_dir_by_parent_dir_and_video_name_and_return_path_name(video_path: str, parent_dir: str) -> str:
    directory = video_path.replace('/Users/popovgleb/PycharmProjects/pythonProject4/video/', '').replace('.mp4', '')
    path = os.path.join(parent_dir, directory)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


# def gg(video_path: str, parent_dir: str):
#     path: str = f'{create_dir_by_parent_dir_and_video_name_and_return_path_name(video_path, parent_dir)}'
#     extract_images(video_path, path)
#     compress_files_from_dir(path)


def get_every_second_of_the_video(video_path: str, root_dir_path: str):
    path = create_dir_by_parent_dir_and_video_name_and_return_path_name(video_path, root_dir_path)
    print(path)
    cmd: str = f"ffmpeg -i {video_path} -r 1 -vf scale=256:256  {path}/image-%05d.jpg"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)


def compress_img(image_path: str):
    cmd: str = f'ffmpeg -i {image_path} -vf scale=256:256 '
    if image_path.endswith('.png'):
        image_name = image_path.replace('.png', '.jpg')
        cmd += f'{image_name}'
    else:
        cmd += f'{image_path}'
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)


def main():
    dir_path: str = '/Users/popovgleb/PycharmProjects/pythonProject4/frams/Шрек_1080/'
    dir_frame_path: str = '/Users/popovgleb/PycharmProjects/pythonProject4/myFrams/'

    video_path: str = '/Users/popovgleb/PycharmProjects/pythonProject4/video/Шрек_1080.mp4'
    photo_path: str = '/Users/popovgleb/PycharmProjects/pythonProject4/myFrams/4.jpg'

    # get_every_second_of_the_video(video_path, '/Users/popovgleb/PycharmProjects/pythonProject4/frams')

    # compress_files_from_dir(dir_frame_path)
    predict(photo_path, dir_path)


if __name__ == '__main__':
    main()
