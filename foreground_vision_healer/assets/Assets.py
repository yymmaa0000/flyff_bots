from pathlib import Path

import cv2 as cv

start_pic_path = str(Path(__file__).parent / "General" / "start.png")
stop_pic_path = str(Path(__file__).parent / "General" / "stop.png")


class GeneralAssets:
    START_PIC = cv.imread(start_pic_path, cv.IMREAD_GRAYSCALE)
    STOP_PIC = cv.imread(stop_pic_path, cv.IMREAD_GRAYSCALE)
