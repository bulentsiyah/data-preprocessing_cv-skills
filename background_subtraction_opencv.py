'''
https://learnopencv.com/background-subtraction-with-opencv-and-bgs-libraries/
'''

import argparse
import cv2


def get_opencv_result(video_to_process):
    # video işleme için VideoCapture nesnesi oluşturun
    captured_video = cv2.VideoCapture(video_to_process)
    # video capture durumunu kontrol et
    if not captured_video.isOpened:
        print("Unable to open: " + video_to_process)
        exit(0)

    # örnek arka plan çıkarma
    background_subtr_method = cv2.bgsegm.createBackgroundSubtractorGSOC()

    while True:
        # video karelerini oku
        retval, frame = captured_video.read()

        # frame lerin tutulup tutulmadığını kontrol edin
        if not retval:
            break

        # video karelerini yeniden boyutlandır
        frame = cv2.resize(frame, (640, 360))

        # frame leri background subtractor a iletin
        foreground_mask = background_subtr_method.apply(frame)
        # ön plan maskesi olmadan arka planı elde edin
        background_img = background_subtr_method.getBackgroundImage()

        # geçerli frame i, ön plan maskesini, çıkarılan sonucu göster
        cv2.imshow("Initial Frames", frame)
        cv2.imshow("Foreground Masks", foreground_mask)
        cv2.imshow("Subtraction Result", background_img)

        keyboard = cv2.waitKey(10)
        if keyboard == 27:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_video",
        type=str,
        help="Define the full input video path",
        default="_videos/space_traffic.mp4",
    )

    # argümentler
    args = parser.parse_args()

    # BS-pipeline başlatın
    get_opencv_result(args.input_video)
