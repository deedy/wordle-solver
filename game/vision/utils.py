import cv2
import numpy as np
import pyautogui
import pyscreenshot as ImageGrab


def get_bb():
    # sourcery skip: inline-immediately-returned-variable, remove-unreachable-code
    # Create a window to display the screen capture
    # cv2.namedWindow("Screen Capture", cv2.WINDOW_FULLSCREEN)

    # Use the ImageGrab module to capture the screen
    img = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_BGR2RGB)

    # Show the captured image
    # cv2.imshow("Screen Capture", img)

    # Wait for the user to select the area containing the wordle
    r = cv2.selectROI(img)
    cv2.destroyAllWindows()

    return r


def take_screenshot(bb):

    img_raw = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_BGR2RGB)

    return img_raw[int(bb[1]):int(bb[1]+bb[3]), int(bb[0]):int(bb[0]+bb[2])]


def show_color(img):

    R, G, B = img[10:11, 10:11, :].ravel()

    if R < 130 and G < 130 and B < 130:
        return 0

    if R < 100 and G > 150 and B > 180:
        return 1

    return 2 if R < 120 and G > 120 and B < 120 else -1


def get_code_from_line(full_grid, line):

    col1 = range(10, 60)
    col2 = range(60, 120)
    col3 = range(120, 170)
    col4 = range(180, 220)
    col5 = range(230, 250)

    cols = [col1, col2, col3, col4, col5]

    if line == 1:
        code = [show_color(full_grid[0:60, col, :]) for col in cols]
    if line == 2:
        code = [show_color(full_grid[60:120, col, :]) for col in cols]
    if line == 3:
        code = [show_color(full_grid[120:170, col, :]) for col in cols]
    if line == 4:
        code = [show_color(full_grid[180:220, col, :]) for col in cols]
    if line == 5:
        code = [show_color(full_grid[240:270, col, :]) for col in cols]
    if line == 6:
        code = [show_color(full_grid[290:350, col, :]) for col in cols]
    return ''.join(map(str, code))


def write_word(word):

    pyautogui.write(word)
    pyautogui.press("enter")
