import os
import cv2
import time
from surround_view import CaptureThread, CameraProcessingThread
from surround_view import FisheyeCameraModel, BirdView
from surround_view import MultiBufferManager, ProjectedImageBuffer
import surround_view.param_settings as settings


yamls_dir = os.path.join(os.getcwd(), "yaml")
camera_ids = [2, 14, 6, 10]
flip_methods = [0, 2, 0, 2]
names = settings.camera_names
cameras_files = [os.path.join(yamls_dir, name + ".yaml") for name in names]
camera_models = [FisheyeCameraModel(camera_file, name) for camera_file, name in zip(cameras_files, names)]


def main():
    capture_tds = [CaptureThread(camera_id, flip_method, resolution=(1280, 720), use_gst=False)
                   for camera_id, flip_method in zip(camera_ids, flip_methods)]
    capture_buffer_manager = MultiBufferManager()
    for td in capture_tds:
        capture_buffer_manager.bind_thread(td, buffer_size=8)
        if (td.connect_camera()):
            print("camera ok")
            td.start()

    proc_buffer_manager = ProjectedImageBuffer()
    process_tds = [CameraProcessingThread(capture_buffer_manager,
                                          camera_id,
                                          camera_model)
                   for camera_id, camera_model in zip(camera_ids, camera_models)]
    for td in process_tds:
        proc_buffer_manager.bind_thread(td)
        print("process buffer mgr ok")
        td.start()

    birdview = BirdView(proc_buffer_manager)
    birdview.load_weights_and_masks("./weights.png", "./masks.png")
    birdview.start()
    time.sleep(3)
    while True:
        print("birdview loop ...")
        data = birdview.get()
        print("birdview get ok...")
        img = cv2.resize(data, (300, 400))
        print("resize ok...")
        cv2.imshow("birdview", img)
        print("imshow ok...")
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        for td in capture_tds:
            print("camera {} fps: {}\n".format(td.device_id, td.stat_data.average_fps), end="\r")

        for td in process_tds:
            print("process {} fps: {}\n".format(td.device_id, td.stat_data.average_fps), end="\r")

        print("birdview fps: {}".format(birdview.stat_data.average_fps))


    for td in process_tds:
        td.stop()

    for td in capture_tds:
        td.stop()
        td.disconnect_camera()


if __name__ == "__main__":
    main()
