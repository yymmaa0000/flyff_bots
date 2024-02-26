from PIL import ImageGrab
from PIL import Image
import cv2 as cv
import numpy as np
import win32con
import win32gui
import win32ui


class WindowCapture:
    def __init__(self, hwnd, crop_area=(8, 30, 8, 8)):
        """
        :param hwnd: int. Handle of the window to capture.
        :param crop_area: tuple (left, top, right, bottom). Area to crop from the window.
                Default: (8, 30, 8, 8) which accounts for the game window border and titlebar.
        """

        self.hwnd = hwnd
        if not self.hwnd:
            raise Exception("Window not found")

        self.crop_l = crop_area[0]
        self.crop_t = crop_area[1]
        self.crop_r = crop_area[2]
        self.crop_b = crop_area[3]

        self.w = 0
        self.h = 0
        self.offset_x = 0
        self.offset_y = 0
        self.__update_size_and_offset()
    
    def get_frame_health_portion(self, bbox=(8, 30, 80, 80)):
        """
        Take a screenshot of the portion of the target window described by the bbox. Works with windows
        foreground. Fullscreen or windowed. But doesn't work with minimized 
        or windows outside the screen.

        :return: PIL img
        """
        image = ImageGrab.grab(bbox)
        #image = image.convert('1', dither=Image.NONE) # Convert PIL img to bw, not useful

        # change all pixel to white if not black for better text recognition
        pixels = image.load()
        for i in range(image.size[0]): # for every pixel:
            for j in range(image.size[1]):
                if pixels[i,j][0] > 210 and pixels[i,j][1] > 210 and pixels[i,j][2] > 210:
                    pixels[i,j] = (0, 0 ,0)
                else:
                    pixels[i,j] = (255, 255 ,255)

        # debug
        image.save("D:\\Projects\\flyff_bots\\foreground_vision_bot\\screenshot.png")
        print("image saved to screenshot.png")

        return image
    
    def get_frame(self):
        """
        Take a screenshot of the target window. Only works with windows in foreground. 
        Fullscreen or windowed. But doesn't work with minimized 
        or windows outside the screen.

        :return: (numpy array, numpy array). The first array is the image in BGR format, 3 channels.
                The second array is the image in grayscale format, 1 channel.
        """

        #image = win32gui.ImageGrab(self.hwnd)
        bbox = win32gui.GetWindowRect(self.hwnd)
        image = ImageGrab.grab(bbox)
        #image.save("D:\screenshot.png")
        
        pil_image = image.convert('RGB') 
        open_cv_image = np.array(pil_image) 
        # Convert RGB to BGR 
        img = open_cv_image[:, :, ::-1].copy()

        # make image C_CONTIGUOUS to avoid errors that look like:
        #   File ... in draw_rectangles
        #   TypeError: an integer is required (got type tuple)
        # see the discussion here:
        # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
        img = np.ascontiguousarray(img)

        # DEBUGGING: Show the image
        #cv.imshow("screenshot", img)
        #cv.waitKey(1)

        # DEBUGGING: Save the screenshot to disk
        #cv.imwrite("screenshot.png", img)

        # Convert image to gray
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        return img, img_gray
    def get_screen_pos(self, pos):
        """
        Translate a pixel position on a screenshot image to a pixel position on the screen.

        :param pos: tuple (x, y). Position on the screenshot image.
        :return: tuple (x, y). Position on the screen.
        """
        self.__update_size_and_offset()
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

    def __update_size_and_offset(self):
        """
        Size doesn't change often, but it's a step to update the offset. Offset
        do change often, it updates when we move the target window.
        """
        # get the window size
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        self.w = right - left - self.crop_l - self.crop_r
        self.h = bottom - top - self.crop_t - self.crop_b

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = left + self.crop_l
        self.offset_y = top + self.crop_t
