import collections
from threading import Thread
from time import sleep, time, gmtime, strftime

import pyttsx3
from assets.Assets import GeneralAssets
from libs.ComputerVision import ComputerVision as CV
from libs.HumanKeyboard import VKEY, HumanKeyboard
from libs.WindowCapture import WindowCapture
from utils.decorators import throttle
from utils.helpers import get_point_nearest_center_3D, start_countdown
from utils.SyncedTimer import SyncedTimer


@throttle()
def emit_msg(gui_window, color, msg):
    gui_window.write_event_value(color, msg)

class Bot:
    def __init__(self):
        self.config = {
            "show_frames": False,
            "show_signal_pos_boxes": False,
            "show_signal_pos_markers": False,
            "show_matches_text": False,
            "signal_match_threshold": 0.9,
            "healing_interval_ms": 1000,
        }
        self.gui_window = None
        self.frame = None
        self.debug_frame = None
        self.__heal_thread_running = False

    def setup(self, window_handler, gui_window):
        self.gui_window = gui_window
        self.voice_engine = pyttsx3.init()
        self.wincap = WindowCapture(window_handler)
        self.keyboard = HumanKeyboard(window_handler)
        Thread(target=self.__frame_thread, daemon=True).start()
        gui_window.write_event_value("msg_green", "Bot is ready.")

    def start(self):
        self.__heal_thread_running = True
        Thread(target=self.__heal_thread, daemon=True).start()

    def stop(self):
        self.__heal_thread_running = False

    def set_config(self, **options):
        """Set the config options for the bot.

        :param **options:
            show_frames: bool
                Show the video frames of the bot. Default: False
            show_signal_pos_boxes: bool
                Show the boxes of the signal positions. Default: False
            show_signal_pos_markers: bool
                Show the markers of the signal positions. Default: False
            show_matches_text: bool
                Show text next to the matches. Default: False
            signal_match_threshold: float
                The threshold to match the signal positions. From 0 to 1. Default: 0.9
            healing_interval_ms: int
                The time to rebuff. Unity in minutes. Default: 10
        """
        for key, value in options.items():
            self.config[key] = value

    def __frame_thread(self):
        """
        Frame thread, it will update the frame and debug_frame variables that will be used by the bot.

        It also execute computer vision functions for debug purposes. The functions results it's not used by the bot.
        """
        fps_circular_buffer = collections.deque(maxlen=10)
        loop_time = time()
        while True:
            try:
                self.debug_frame, self.frame = self.wincap.get_frame()
            except Exception as e:
                emit_msg(
                    _throttle_sec=15,
                    gui_window=self.gui_window,
                    color="msg_red",
                    msg="Error getting the frame. Check if window is visible and attach again.",
                )
                print(f"Error getting the frame. Check if window is visible and attach again. {e}")
                sleep(3)
                continue

            if self.config["show_frames"]:
                matches = self.__detect_visual_signal(GeneralAssets.START_PIC, debug=True)
                self.gui_window.write_event_value("debug_frame", self.debug_frame)

            fps_circular_buffer.append(time() - loop_time)
            fps = round(1 / (sum(fps_circular_buffer) / len(fps_circular_buffer)))
            self.gui_window.write_event_value("video_fps", f"Video FPS: {fps}")
            loop_time = time()

    def __heal_thread(self):
        printMsg = True

        if printMsg:
            print("Heal thread is now running. Awaiting for start signal.")
        isHealing = False;
        healingInterval = float(self.config["healing_interval_ms"]) / 1000.0
        while True:
            if isHealing:
                self.keyboard.hold_key(VKEY["3"], press_time=0.06) # cast heal
                matches = self.__detect_visual_signal(GeneralAssets.STOP_PIC)
                if matches:
                    isHealing = False
                    if printMsg:
                        print("Stop signal detected. Healing ends.")
                sleep(healingInterval)
            else:
                matches = self.__detect_visual_signal(GeneralAssets.START_PIC)
                if matches:
                    isHealing = True
                    if printMsg:
                        print("Start signal detected. Healing begins.")
                sleep(0.5)

            if not self.__heal_thread_running:
                break

        if printMsg:
            print("Heal thread is stopped.")

    """Match Methods"""

    def __detect_visual_signal(self, signal_template, debug=False):
        # focus on the bottom left side of the frame
        matches, drawn_frame = CV.match_template_multi(
            frame=self.frame,
            crop_area=(375, 0, 0, -750),
            template=signal_template,
            threshold=float(self.config["signal_match_threshold"]),
            box_offset=(0, 0),
            frame_to_draw=self.debug_frame if debug else None,
            draw_rect=self.config["show_signal_pos_boxes"],
            draw_marker=self.config["show_signal_pos_markers"],
            draw_text=self.config["show_matches_text"],
        )
        if debug:
            self.debug_frame = drawn_frame

        return matches

    