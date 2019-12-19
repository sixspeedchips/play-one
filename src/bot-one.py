import cv2
# import mouse
import numpy as np
from ahk import AHK
from mss import mss
from win32api import GetSystemMetrics

from position import Position

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

bbox_width = 500
bbox_height = 500
offset_x = + width / 2
offset_y = + height / 2

bounding_box = {'top': int(-bbox_height / 2 + offset_y),
                'left': int(-bbox_width / 2 + offset_x),
                'width': bbox_width, 'height': bbox_height}

# center_x = bounding_box['top'] + bounding_box['height'] / 2
# center_y = bounding_box['left'] + bounding_box['width'] / 2


sct = mss()
# mouse = Controller()
scale = 1
idx = 0
ahk = AHK()


def move(x, y):
    # mouse.move(coords=(x,y))
    pass


def calc_x(pos):
    r = int(1 * (250 - pos.x))
    return r


def calc_y(pos):
    r = int(1 * (250 - pos.y))
    return r


def green_filter(img, sensitivity=10):
    green = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_green = np.array([60 - sensitivity, 100, 100])
    upper_green = np.array([60 + sensitivity, 255, 255])
    mask = cv2.inRange(green, lower_green, upper_green)
    green[np.where(mask == 0)] = 0
    return green


def red_filter(img,sensitivity=2):
    red = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0 - sensitivity, 50, 50])
    upper_red = np.array([10 + sensitivity, 255, 255])
    mask0 = cv2.inRange(red, lower_red, upper_red)
    lower_red = np.array([170 - sensitivity, 50, 50])
    upper_red = np.array([180 + sensitivity, 255, 255])
    mask1 = cv2.inRange(red, lower_red, upper_red)
    mask = cv2.bitwise_or(mask0, mask1)
    red[np.where(mask == 0)] = 0
    return red

def filter_reticle(img, sensitivity=1):
    reticule = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_ret = np.array([91 - sensitivity, 100, 100])
    upper_ret = np.array([91 + sensitivity, 255, 255])
    mask = cv2.inRange(reticule, lower_ret, upper_ret)
    reticule[np.where(mask == 0)] = 0
    return reticule

if __name__ == '__main__':
    pos = Position(250, 250, 1)
    while True:
        idx += 1
        sct_img = sct.grab(bounding_box)
        img = np.array(sct_img)
        # img = cv2.resize(img, (1000, 1000), interpolation=cv2.INTER_AREA)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img_c = cv2.Canny(img, 125, 150)

        filtered = red_filter(img, sensitivity=2)

        img_c = cv2.Canny(filtered, 125, 150)
        contours, hierarchy = cv2.findContours(img_c, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
        ct = []
        cv2.cvtColor(filtered, cv2.COLOR_HSV2BGR, filtered)

        # for cnt in contours:
        #     approx = cv2.approxPolyDP(cnt, 0.05 * cv2.arcLength(cnt, True),True)
        #     if len(approx) == 3:
        #         # print("found")
        #         M = cv2.moments(cnt)
        #         cX = int(M["m10"] / M["m00"])
        #         cY = int(M["m01"] / M["m00"])
        #         cv2.circle(filtered, (cX, cY), 10, (0, 0, 255), -1)
        #         cv2.drawContours(filtered, [cnt], 0, (0,0, 255), 2)
        #         tri = approx
        # cv2.drawContours(img, ct, -1, (0, 0, 255), 3)

        # cv2.threshold(green, 165, 255, cv2.THRESH_BINARY, green)
        green = filter_reticle(img, sensitivity=2)
        cv2.cvtColor(green, cv2.COLOR_HSV2BGR, green)
        green = cv2.Canny(green, 125, 150)
        # grey = cv2.cvtColor(green, cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(green, cv2.HOUGH_GRADIENT, 2.5, 100,
                                   minRadius=25, maxRadius=30)
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

            for (x, y, r) in circles:
                pos.x = x
                pos.y = y
                pos.r = r
            print(pos)

        cv2.circle(green, (pos.x, pos.y), pos.r, (0, 255, 0), 4)
        cv2.rectangle(green, (pos.x - 5, pos.y - 5), (pos.x + 5, pos.y + 5),
                      (0, 128, 255), -1)
        # filtered = cv2.resize(img, (500, 500), interpolation=cv2.INTER_AREA)
        # filtered = cv2.resize(filtered, (500, 500), interpolation=cv2.INTER_AREA)
        cv2.imshow('screen', green)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break
