import cv2
import os
import numpy as np
from copy import deepcopy

clicks = []
click_counter = 0


def _click_callback(event, x, y, flags, param):
    """Callback function for mouse click events."""
    global click_counter
    global clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        clicks.append((x, y))
        click_counter -= 1


def click_on_image(image, times=1, mark=False, delay=100, text='Click on image', counter=True):
    """
    Prompt the user with a window to click predetermined times to complete action.

    :param image: np.array, image to show the user
    :param times: int, number of clicks requested from the user
    :param mark: bool, leave a mark on the image where clicked
    :param delay: int, refresh rate in milliseconds before image refresh
    :param text: str, text to show on the window
    :param counter: bool, show click counter if True
    :return: np.array, array of clicked coordinates
    """
    img = deepcopy(image)
    if len(img.shape) == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    scale = get_scale(img)
    global clicks
    global click_counter
    clicks = []
    click_counter = times
    while click_counter > 0:
        if mark and clicks:
            for x, y in clicks:
                cv2.circle(img, (int(x / scale), int(y / scale)), int(img.shape[0] / 100.0), (255, 255, 255), 3)
                cv2.circle(img, (int(x / scale), int(y / scale)), int(img.shape[0] / 100.0), (0, 0, 0), -1)
        display_text = f'({times - click_counter}/{times}) - {text}' if counter else text
        cv2.namedWindow(display_text)
        cv2.setMouseCallback(display_text, _click_callback)
        k = show_image(img, text=display_text, destroy=False, time=delay)
        if k != -1:
            cv2.destroyAllWindows()
            return k
    cv2.destroyAllWindows()
    out_clicks = deepcopy(clicks)
    clicks = []
    return np.asarray(np.array(out_clicks) / scale, dtype=int)


def get_scale(image, max_dimensions=(750, 1200)):
    """
    Calculate the scale factor to resize an image to fit within max dimensions.

    :param image: np.array, the image to be scaled
    :param max_dimensions: tuple of int, maximum width and height dimensions
    :return: float, scale factor
    """
    dims = image.shape[:2]
    scale = min(max_dimensions[0] / dims[0], max_dimensions[1] / dims[1])
    return scale


def show_image(image, text='Image', time=0, destroy=True):
    """
    Display an image in a window.

    :param image: np.array, the image to display
    :param text: str, window title
    :param time: int, duration to wait for a key event
    :param destroy: bool, whether to destroy all windows after showing the image
    :return: int, ASCII code of the key pressed or -1 if no key is pressed
    """
    if os.uname().sysname == 'Linux' and 'armv7l' in os.uname().machine:
        return
    scale = get_scale(image)
    resized_image = cv2.resize(image, None, fx=scale, fy=scale)
    cv2.imshow(text, resized_image)
    k = cv2.waitKey(time) & 0xFF
    if destroy:
        cv2.destroyAllWindows()
    return k