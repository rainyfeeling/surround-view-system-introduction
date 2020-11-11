#!/usr/bin/env python3

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

def show_cam_img(caps, cam_list):
    DEBUG=0

    idx = 0
    cnt = 0
    while True:
        ret = False
        cap_device = caps[idx]
        if (cap_device.grab()):
            ret, frame = cap_device.retrieve()

            if DEBUG:
                arr = frame.tobytes()
                # first 8 bytes
                print("%02x %02x %02x %02x  %02x %02x %02x %02x" %(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7]))
                # last 8 bytes
                arr = arr[-8:]
                print("%02x %02x %02x %02x  %02x %02x %02x %02x" %(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7]))
        if ret:
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow('video', frame)
        else:
            print("failed read frame!")

        c = cv2.waitKey(1)
        if c == ord('q'):
            break
        if c == ord('c'):
            idx += 1
            if idx >= len(caps):
                idx = 0
            continue
        if c == ord('s'):
            # save the picture
            if ret:
                name = 'video{}_{}.png'.format(cam_list[idx], cnt)
                cv2.imwrite(name, frame)
                print("saved file: %s!" %name)
                cnt += 1

    cv2.destroyAllWindows()

def init_caps(cam_list, resolution=(1280,720)):
    caps = []
    for iCam in cam_list:
        cap = cv2.VideoCapture(iCam)
        if not cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G')):
            print("Failed to set PROP_FOURCC!")

        if not cap.set(3, resolution[0]):
            print("Failed to set PROP_WIDTH!")

        if not cap.set(4, resolution[1]):
            print("Failed to set PROP_HEIGHT!")

        if not cap.set(cv2.CAP_PROP_CONVERT_RGB, 0.0):
            print("Failed to set PROP_CONVERT_RGB!")

        caps.append(cap)

    return caps

def deinit_caps(cap_list):
    for cap in cap_list:
        cap.release()

def main():
    cam_list = get_cam_lst([2, 6, 10, 14])
    print("avaliable list is {}".format(cam_list))

    caps = init_caps(cam_list)

    show_cam_img(caps, cam_list)

    deinit_caps(caps)

if __name__ == "__main__":
    main()
