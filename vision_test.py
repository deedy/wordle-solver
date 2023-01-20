import time
import cv2
import pyautogui
import numpy as np
# from PIL import ImageGrab
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

    # # Crop the image to the selected area
    # wordle = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

    # # Close the window and return the cropped image
    # return wordle


def take_screenshot(bb, file_name):

    img_raw = cv2.cvtColor(np.array(ImageGrab.grab()), cv2.COLOR_BGR2RGB)

    roi_cropped = img_raw[int(bb[1]):int(bb[1]+bb[3]), int(bb[0]):int(bb[0]+bb[2])]
    # Save the screenshot as a PNG image
    cv2.imwrite(f'images/{file_name}', roi_cropped)


def segment_rows(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to the image to create a binary image
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Apply edge detection to the binary image
    edges = cv2.Canny(thresh, 50, 150)

    # Find the contours in the image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize an empty list to store the segmented rows
    rows = []

    # Iterate through the contours and find the bounding rectangles
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Append the segmented row to the list
        rows.append(img[y:y+h, x:x+w])

    return rows


if __name__ == "__main__":
    # take_screenshot('first_row.png')

    # bb = get_bb()
    # print(bb)
    # take_screenshot(bb, 'game_grid.png')

    game_grid = np.array(cv2.imread('images/game_grid.png'))
    print(game_grid)

    # rows = segment_rows(game_grid)

    # print(rows)

# soare = cv2.imread('images/soare.png')

# cv2.imshow('soare', soare)

# cv2.waitKey(0)
