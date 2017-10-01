import cv2
import os
import numpy as np
from copy import copy

clicks = []
click_counter = 0


def _click_callback(event, x, y, flags, param):
    global click_counter
    global clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        clicks.append((x, y))
        click_counter -= 1


def click_on_image(image, times=1, mark=None, delay=100, text='image'):
    img = image.copy()
    if len(img.shape) == 2:
        img = np.stack([img] * 3, -1)
    scale = get_scale(img)
    cv2.namedWindow(text)
    cv2.setMouseCallback(text, _click_callback)
    global clicks
    global click_counter
    clicks = []
    click_counter = times
    while click_counter > 0:
        if mark is not None and len(clicks) > 0:
            img[int(clicks[-1][1] / scale), int(clicks[-1][0] / scale)] = mark
        k = show_image(img, text=text, destroy=False, time=delay)
        if k != -1:
            cv2.destroyAllWindows()
            return k
    cv2.destroyAllWindows()
    out_clicks = copy(clicks)
    clicks = []
    out_clicks = np.asarray(np.array(out_clicks) / scale, dtype=int)
    return out_clicks


def get_scale(image, max_dimensions=(750, 1200)):
    '''
    Given an image and maximum display dimensions,
    get_scale returns a scale factor corresponding to the
    optimal image size reduction to fit to the screen.
    '''
    dims = image.shape
    if 0 in dims:
        raise TypeError('Cannot show image without dimensions')
    scale = min([
        float(max_dimensions[0]) / dims[0],
        float(max_dimensions[1]) / dims[1]])
    return scale


def show_image(image, text='Image', time=0, destroy=True):
    if os.uname()[0] == 'Linux':
        return
    scale = get_scale(image)
    resized_image = image.copy()
    resized_image = cv2.resize(resized_image, None, fx=scale, fy=scale)
    cv2.imshow(str(text), resized_image)
    k = cv2.waitKey(time)
    if destroy:
        cv2.destroyAllWindows()
    return k
