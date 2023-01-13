import numpy as np


class Image(object):

    def __init__(self, image_cv2, height: int, width: int):
        self.image_cv2 = image_cv2
        self.height: int = height
        self.width: int = width

    def get_central_pixel(self) -> [[int]]:
        h: int = self.height
        w: int = self.width
        central_pixel = self.image_cv2[int(h / 2)][int(w / 2)]
        list_pixel = np.array([central_pixel])
        return list_pixel

    def compare(self, array: [[int]]) -> bool:
        return np.allclose(self.get_central_pixel(), array, atol=15)
