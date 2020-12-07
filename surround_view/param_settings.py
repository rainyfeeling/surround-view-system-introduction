import os
import cv2


camera_names = ["front", "back", "left", "right"]

# --------------------------------------------------------------------
# (shift_width, shift_height): how far away the birdview looks outside
# of the calibration pattern in horizontal and vertical directions
shift_w = 100
shift_h = 100

# size of the gap between the calibration pattern and the car
# in horizontal and vertical directions
inn_shift_w = 10
inn_shift_h = 10

# total width/height of the stitched image
# total_w = 620, total_h = 580
total_w = 420 + 2 * shift_w
total_h = 380 + 2 * shift_h

# four corners of the rectangular region occupied by the car
# top-left (x_left, y_top), bottom-right (x_right, y_bottom)
# xl = 210, xr = 410, yt = 210, yb = 370
xl = shift_w + 100 + inn_shift_w
xr = total_w - xl
yt = shift_h + 100 + inn_shift_h
yb = total_h - yt
# --------------------------------------------------------------------

project_shapes = {
    # front - (620 x 210)
    "front": (total_w, yt),
    "back":  (total_w, yt),
    "left":  (total_h, xl),
    "right": (total_h, xl)
}

# pixel locations of the four points to be choosen.
# you must click these pixels in the same order when running
# the get_projection_map.py script
project_keypoints = {
    # [_topleft(200, 100), _topright(420, 100), _bottomleft(200, 200), _bottomright(420, 200)]
    "front": [(shift_w + 100, shift_h),
              (shift_w + 320, shift_h),
              (shift_w + 100, shift_h + 100),
              (shift_w + 320, shift_h + 100)],

    "back":  [(shift_w + 100, shift_h),
              (shift_w + 320, shift_h),
              (shift_w + 100, shift_h + 100),
              (shift_w + 320, shift_h + 100)],

    "left":  [(shift_h + 100, shift_w),
              (shift_h + 280, shift_w),
              (shift_h + 100, shift_w + 100),
              (shift_h + 280, shift_w + 100)],

    "right": [(shift_h + 100, shift_w),
              (shift_h + 280, shift_w),
              (shift_h + 100, shift_w + 100),
              (shift_h + 280, shift_w + 100)]
}

car_image = cv2.imread(os.path.join(os.getcwd(), "images", "car.png"))
car_image = cv2.resize(car_image, (xr - xl, yb - yt))
