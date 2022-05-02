import time
import cv2
import numpy as np
import pytesseract
from matplotlib import pyplot as plt

from Emulator import Emulator, tap_profile, tap_rankings, tap_individual_power

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def remove_noise(image):
    return cv2.GaussianBlur(image, (5, 5), 0)


def thresholding(image):
    return cv2.threshold(image, -5000, 255, cv2.THRESH_OTSU)[1]


def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


def canny(image):
    return cv2.Canny(image, 100, 200)


def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)

    else:
        angle = -angle
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        m = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, m, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


if __name__ == '__main__':
    emulator = Emulator()
    emulator.connect()

    with open('gov_info.png', 'wb') as f:
        f.write(emulator.screenshot())

    image = cv2.imread('gov_info.png')

    image_grey = get_grayscale(image)

    roi_gov_id = (1240, 380, 300, 40)
    roi_gov_name = (1025, 425, 600, 60)
    roi_alliance = (1035, 590, 400, 40)

    gov_id_img = image_grey[roi_gov_id[1]:roi_gov_id[1] + roi_gov_id[3], roi_gov_id[0]:roi_gov_id[0] + roi_gov_id[2]]
    gov_name_img = image_grey[roi_gov_name[1]:roi_gov_name[1] + roi_gov_name[3],
                   roi_gov_name[0]:roi_gov_name[0] + roi_gov_name[2]]
    alliance_img = image_grey[roi_alliance[1]:roi_alliance[1] + roi_alliance[3],
                   roi_alliance[0]:roi_alliance[0] + roi_alliance[2]]

    gov_id_img = thresholding(gov_id_img)
    gov_name_img = thresholding(gov_name_img)
    alliance_img = thresholding(alliance_img)

    cv2.imshow('img', gov_id_img)

    print(pytesseract.image_to_string(gov_id_img, config='-c tessedit_char_whitelist=0123456789'))
    print(pytesseract.image_to_string(gov_name_img))
    print(pytesseract.image_to_string(alliance_img))

    while True:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
