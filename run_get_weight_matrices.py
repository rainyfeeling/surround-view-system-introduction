import os
import numpy as np
import cv2
from PIL import Image
from surround_view import FisheyeCameraModel, display_image, BirdView
import surround_view.param_settings as settings


def main():
    names = settings.camera_names
    images = [os.path.join(os.getcwd(), "images", name + ".png") for name in names]
    yamls = [os.path.join(os.getcwd(), "yaml", name + ".yaml") for name in names]
    camera_models = [FisheyeCameraModel(yaml_file, camera_name) for yaml_file, camera_name in zip (yamls, names)]

    projected = []
    i = 0
    for image_file, camera in zip(images, camera_models):
        img = cv2.imread(image_file)
        img = camera.undistort(img)
        img = camera.project(img)
        img = camera.flip(img)
        projected.append(img)
        ret = display_image("projected {0}".format(image_file), img)
        cv2.imwrite(names[i] + '_bird' + '.png', img)
        # if user enter 'q' then exit
        if ret < 0:
            return ret
        i += 1

    birdview = BirdView()
    Gmat, Mmat = birdview.get_weights_and_masks(projected)
    birdview.update_frames(projected)
    birdview.make_luminance_balance().stitch_all_parts()
    birdview.make_white_balance()
    birdview.copy_car_image()
    ret = display_image("BirdView Result", birdview.image)
    if ret > 0:
        Image.fromarray((Gmat * 255).astype(np.uint8)).save("weights.png")
        Image.fromarray(Mmat.astype(np.uint8)).save("masks.png")
        cv2.imwrite('all.png', birdview.image)


if __name__ == "__main__":
    main()
