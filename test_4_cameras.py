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

def show_cam_img(cap_device):
    while True:
        ret, frame = cap_device.read()
        if ret:
            cv2.imshow('video', frame)
        else:
            print("failed read frame!")

        c = cv2.waitKey(1)
        if c == ord('q'):
            break

    cv2.destroyAllWindows()

def init_caps(cam_list):
    caps = []
    for iCam in cam_list:
        cap = cv2.VideoCapture(iCam)
        caps.append(cap)

    return caps

def deinit_caps(cap_list):
    for cap in cap_list:
        cap.release()

def main():
    cam_list = get_cam_lst([2, 6, 10, 14])
    print("avaliable list is {}".format(cam_list))

    caps = init_caps(cam_list)

    show_cam_img(caps[0])

    deinit_caps(caps)

if __name__ == "__main__":
    main()
