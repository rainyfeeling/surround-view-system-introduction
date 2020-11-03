import os
import cv2
import time

# get the installed camera list for initialization.
def get_cam_lst(cam_lst=range(0, 24)):
    arr = []
    for iCam in cam_lst:
        cap = cv2.VideoCapture(iCam)
        if not cap.read()[0]:
            continue
        else:
            arr.append(iCam)

        cap.release()
    return arr

def main():
    cam_list = get_cam_lst([2, 6, 10, 14])
    print("avaliable list is {}".format(cam_list))

if __name__ == "__main__":
    main()
