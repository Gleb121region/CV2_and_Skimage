import fnmatch
import os

import cv2
from PIL import Image
from skimage.metrics import structural_similarity as ssim


def predict(file_path: str, name_dir: str):
    for image_name in give_name_file(name_dir):
        path = name_dir + image_name
        img = cv2.imread(file_path)
        try:
            ref = cv2.imread(path)
            gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
            (simular, diff) = ssim(gray1, gray2, full=True)
            if simular > 0.5:
                print(simular)
                print(path)
        except:
            print('похуй')


def give_name_file(name_dir: str) -> [str]:
    listOfFiles = os.listdir(name_dir)
    pattern = "*.jpg"
    list_name_photo = []
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
            list_name_photo.append(entry)
    return listOfFiles


def extractImages(pathIn: str, pathOut: str):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)
    success, image = vidcap.read()
    success = True
    while success:
        try:
            vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))
            success, image = vidcap.read()
            cv2.imwrite(pathOut + "frame%d.jpg" % count, image)
            count = count + 1
        except:
            print('все')


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


if __name__ == "__main__":
    name_dir: str = 'frams/'
    name_dir_frame: str = '/Users/popovgleb/PycharmProjects/pythonProject4/myFrams/'

    predict('/Users/popovgleb/PycharmProjects/pythonProject4/myFrams/Снимок экрана 2023-01-11 в 14.01.58.jpg',
            name_dir)

# extractImages(pathIn='/Users/popovgleb/PycharmProjects/pythonProject4/video/Друзья_S10_E2_1080.mp4',
#               pathOut=name_dir)
# for image_name in give_name_file(name_dir):
#     path = name_dir + image_name
#     print(path)
#     try:
#         compress_img(image_name=path, new_size_ratio=0.9, quality=75, width=2880, height=1800, to_jpg=True)
#     except:
#         print("похуй")

# for image_name in give_name_file(name_dir_frame):
#     path = name_dir_frame + image_name
#     print(path)
#     try:
#         compress_img(image_name=path, new_size_ratio=200, quality=75, width=1152, height=648, to_jpg=True)
#     except:
#         print('похуй')
