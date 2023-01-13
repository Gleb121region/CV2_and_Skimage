import os
import pathlib

import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim


def give_list_frame_path(name_dir: str) -> [str]:
    res = []
    d = pathlib.Path(name_dir)
    for entry in d.iterdir():
        if entry.is_file():
            res.append(str(entry))
    return res


def mse(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


def predict(file_path: str, folder_path: str):
    tmp_simular_cof = -1
    tmp_mse = float(10000)

    for image_name in give_list_frame_path(folder_path):
        img = cv2.imread(file_path)
        ref = cv2.imread(image_name)
        gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
        (simular, diff) = ssim(gray1, gray2, full=True)
        mse_cof = mse(img, ref)
        if simular > tmp_simular_cof:
            tmp_simular_cof = simular
            print(image_name)

        if mse_cof < tmp_mse:
            tmp_mse = mse_cof
            print(mse_cof)
            print(image_name)
    print(f'mse: {tmp_mse} \n simular: {tmp_simular_cof}')


def extract_images(path_in: str, path_out: str):
    count = 0
    video_capture = cv2.VideoCapture(path_in)
    success, image = video_capture.read()
    success = True
    while success:
        try:
            video_capture.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
            success, image = video_capture.read()
            photo_path = path_out + "frame%d.jpg" % count
            cv2.imwrite(photo_path, image)
            count = count + 1
        except:
            print('The video is over')


def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def compress_img(image_name, new_size_ratio, quality, width=None, height=None, to_jpg=True):
    img = Image.open(image_name)
    print("[*] Image shape:", img.size)
    image_size = os.path.getsize(image_name)
    print("[*] Size before compression:", get_size_format(image_size))
    if new_size_ratio < 1.0:
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
        print("[+] New Image shape:", img.size)
    elif width and height:
        img = img.resize((width, height), Image.ANTIALIAS)
        print("[+] New Image shape:", img.size)
    filename, ext = os.path.splitext(image_name)
    if to_jpg:
        new_filename = f"{filename}.jpg"
    else:
        new_filename = f"{filename}{ext}"
    try:
        img.save(new_filename, quality=quality, optimize=True)
    except OSError:
        img = img.convert("RGB")
        img.save(new_filename, quality=quality, optimize=True)
    print("[+] New file saved:", new_filename)
    new_image_size = os.path.getsize(new_filename)
    print("[+] Size after compression:", get_size_format(new_image_size))
    saving_diff = new_image_size - image_size
    print(f"[+] Image size change: {saving_diff / image_size * 100:.2f}% of the original image size.")


def compress_files_from_dir(dir_name: str) -> None:
    for image_name in give_list_frame_path(dir_name):
        try:
            compress_img(image_name=image_name, new_size_ratio=1, quality=75, width=256, height=256, to_jpg=True)
        except:
            pass


def create_dir_by_parent_dir_and_video_name_and_return_path_name(video_path: str, parent_dir: str) -> str:
    directory = video_path.replace('/Users/popovgleb/PycharmProjects/pythonProject4/video/', '').replace('.mp4', '')
    path = os.path.join(parent_dir, directory)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def gg(video_path: str, parent_dir: str):
    path: str = f'{create_dir_by_parent_dir_and_video_name_and_return_path_name(video_path, parent_dir)}'
    extract_images(video_path, path)
    compress_files_from_dir(path)

# def ffmpeg(video_path:str , root_dir_path:str):
#     "ffmpeg -i Шрек_1080.mp4 -r 1 -vf scale=256:256  image-%05d.jpeg"

def main():
    dir_path: str = '/Users/popovgleb/PycharmProjects/pythonProject4/frams/Шрек_1080/'
    dir_frame_path: str = '/Users/popovgleb/PycharmProjects/pythonProject4/myFrams/'

    photo_path: str = '/Users/popovgleb/PycharmProjects/pythonProject4/myFrams/Снимок экрана 2023-01-13 в 02.41.02.jpg'

    compress_files_from_dir(dir_frame_path)
    predict(photo_path, dir_path)


if __name__ == '__main__':
    main()
