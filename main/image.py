import numpy as np


class Image(object):

    def __init__(self, image_cv2, height: int, width: int):
        self.image_cv2 = image_cv2
        self.height: int = height
        self.width: int = width

    def main_pixels(self) -> [[int]]:
        h: int = self.height
        w: int = self.width
        # height_left_pixel = self.image_cv2[0][0]
        # low_left_pixel = self.image_cv2[h - 1][0]
        # height_right_pixel = self.image_cv2[0][w - 1]
        # low_right_pixel = self.image_cv2[h - 1][w - 1]
        central_pixel = self.image_cv2[int(h / 2)][int(w / 2)]

        # list_pixel = np.array([height_left_pixel, low_left_pixel, height_right_pixel, low_right_pixel, central_pixel])
        list_pixel = np.array([central_pixel])
        return list_pixel

    def compare(self, array: [[int]]) -> bool:
        if np.array_equal(self.main_pixels(), array):
            return  True
        # assert all(np.isclose(self.main_pixels(), array) for i in range(self.width))
