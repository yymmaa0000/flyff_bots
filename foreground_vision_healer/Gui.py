import difflib

import cv2 as cv
import PySimpleGUI as sg
from utils.helpers import get_window_handlers, hex_variant


class Gui:
    def __init__(self, theme="DarkAmber"):
        self.logger_events = ["msg", "msg_red", "msg_purple", "msg_blue", "msg_green"]
        self.logger_events_color = {
            "msg": ("white", "black"),
            "msg_red": ("white", "red"),
            "msg_purple": ("white", "purple"),
            "msg_blue": ("white", "blue"),
            "msg_green": ("white", "green"),
        }
        self.frame_resolutions = {
            "160x120": (160, 120),
            "200x150": (200, 150),
            "320x240": (320, 240),
            "400x300": (400, 300),
            "640x480": (640, 480),
            "800x600": (800, 600),
            "1024x600": (1024, 600),
            "1024x768": (1024, 768),
            "1280x700": (1280, 700),
            "1280x720": (1280, 720),
            "1280x800": (1280, 800),
            "1280x1024": (1280, 1024),
            "1366x768": (1366, 768),
        }
        sg.theme(theme)

    def init(self):
        layout = self.__get_layout()
        self.window = sg.Window("Flyff Vision Healer", layout, location=(0, 0), resizable=True, finalize=True)
        sg.cprint_set_output_destination(self.window, "-ML-")
        sg.user_settings_filename(path=".")
        self.__set_hotkeys()
        return self.window

    def loop(self, bot):
        self.__load_settings(bot)
        while True:
            event, values = self.window.read(timeout=1000)

            # ACTIONS - Button events
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            if event == "-ATTACH_WINDOW-":
                game_window_name, game_window_handler = self.__attach_window_popup()
                if game_window_name and game_window_handler:
                    bot.stop()
                    bot.setup(game_window_handler, self.window)
                    truncated_game_window_name = (
                        game_window_name[:30] + "..." if len(game_window_name) > 30 else game_window_name
                    )
                    self.window["-ATTACHED_WINDOW-"].update(truncated_game_window_name)
                    self.window["-START_BOT-"].update(disabled=False)
                    self.window["-STOP_BOT-"].update(disabled=True)
            if event == "-START_BOT-":
                bot.start()
                self.window["-START_BOT-"].update(disabled=True)
                self.window["-STOP_BOT-"].update(disabled=False)
            if event == "-STOP_BOT-":
                bot.stop()
                self.window["-START_BOT-"].update(disabled=False)
                self.window["-STOP_BOT-"].update(disabled=True)

            # BOT OPTIONS - Video options
            if event == "-SHOW_FRAMES-":
                bot.set_config(show_frames=values["-SHOW_FRAMES-"])
                self.window["-SHOW_MATCHES_TEXT-"].update(visible=(values["-SHOW_FRAMES-"]))
                self.window["-SHOW_BOXES-"].update(visible=(values["-SHOW_FRAMES-"]))
                self.window["-SHOW_MARKERS-"].update(visible=(values["-SHOW_FRAMES-"]))
                self.window["-VISION_FRAME-"].update(visible=(values["-SHOW_FRAMES-"]))
                self.window.refresh()  # Combined with contents_changed, will compute the new size of the element
                self.window["-MAIN_COLUMN-"].contents_changed()
            if event == "-SHOW_MATCHES_TEXT-":
                bot.set_config(show_matches_text=values["-SHOW_MATCHES_TEXT-"])
                sg.user_settings_set_entry("-SHOW_MATCHES_TEXT-", values["-SHOW_MATCHES_TEXT-"])
            if event == "-SHOW_BOXES-":
                bot.set_config(show_signal_pos_boxes=values["-SHOW_BOXES-"])
                sg.user_settings_set_entry("-SHOW_BOXES-", values["-SHOW_BOXES-"])
            if event == "-SHOW_MARKERS-":
                bot.set_config(show_signal_pos_markers=values["-SHOW_MARKERS-"])
                sg.user_settings_set_entry("-SHOW_MARKERS-", values["-SHOW_MARKERS-"])

            # BOT OPTIONS - General options
            if event == "-SIGNAL_MATCH_THRESHOLD-":
                bot.set_config(signal_match_threshold=values["-SIGNAL_MATCH_THRESHOLD-"])
                sg.user_settings_set_entry("-SIGNAL_MATCH_THRESHOLD-", values["-SIGNAL_MATCH_THRESHOLD-"])
            if event == "-HEALING_INTERVAL_MS-":
                try:
                    healing_interval_ms = float(values["-HEALING_INTERVAL_MS-"])
                    bot.set_config(healing_interval_ms=healing_interval_ms)
                    sg.user_settings_set_entry(
                        "-HEALING_INTERVAL_MS-", values["-HEALING_INTERVAL_MS-"]
                    )
                except ValueError:
                    sg.cprint("Invalid rebuff timer, must be in minutes")
                    self.window["-HEALING_INTERVAL_MS-"].update("1000")
                    bot.set_config(healing_interval_ms=30)
                    sg.user_settings_set_entry("-HEALING_INTERVAL_MS-", "1000")

            # STATUS - Text events
            if event in self.logger_events:
                sg.cprint(values[event], c=self.logger_events_color[event])
            if event == "video_fps":
                self.window["-VIDEO_FPS-"].update(values["video_fps"])

            # VIDEO - Bot's Vision
            if values["-SHOW_FRAMES-"]:
                img = values.get("debug_frame", None)
                if img is not None:
                    resolution = values["-DEBUG_IMG_WIDTH-"]
                    w, h = self.frame_resolutions[resolution]
                    img = cv.resize(img, (w, h))
                    imgbytes = cv.imencode(".png", img)[1].tobytes()
                    self.window["-DEBUG_IMAGE-"].update(data=imgbytes)

    def close(self):
        self.window.close()

    def __load_settings(self, bot):
        show_matches_text = sg.user_settings_get_entry("-SHOW_MATCHES_TEXT-", False)
        self.window["-SHOW_MATCHES_TEXT-"].update(show_matches_text)
        bot.set_config(show_matches_text=show_matches_text)

        show_signal_pos_boxes = sg.user_settings_get_entry("-SHOW_BOXES-", False)
        self.window["-SHOW_BOXES-"].update(show_signal_pos_boxes)
        bot.set_config(show_signal_pos_boxes=show_signal_pos_boxes)

        show_signal_pos_markers = sg.user_settings_get_entry("-SHOW_MARKERS-", False)
        self.window["-SHOW_MARKERS-"].update(show_signal_pos_markers)
        bot.set_config(show_signal_pos_markers=show_signal_pos_markers)

        signal_match_threshold = sg.user_settings_get_entry("-SIGNAL_MATCH_THRESHOLD-", 0.9)
        self.window["-SIGNAL_MATCH_THRESHOLD-"].update(signal_match_threshold)
        bot.set_config(signal_match_threshold=signal_match_threshold)

        healing_interval_ms = sg.user_settings_get_entry("-HEALING_INTERVAL_MS-", "1000")
        self.window["-HEALING_INTERVAL_MS-"].update(healing_interval_ms)
        bot.set_config(healing_interval_ms=healing_interval_ms)

    def __set_hotkeys(self):
        self.window.bind("<Alt_L><s>", "-STOP_BOT-")

    def __get_layout(self):
        def Collapsible(layout, key, title="", collapsed=False):
            """
            User Defined Element
            A "collapsable section" element. Like a container element that can be collapsed and brought back
            :param layout:Tuple[List[sg.Element]]: The layout for the section
            :param key:Any: Key used to make this section visible / invisible
            :param title:str: Title to show next to arrow
            :param collapsed:bool: If True, then the section begins in a collapsed state
            :return:sg.Column: Column including the arrows, title and the layout that is pinned
            """
            arrows = (sg.SYMBOL_DOWN, sg.SYMBOL_UP)
            return sg.Column(
                [
                    [
                        sg.T((arrows[1] if collapsed else arrows[0]), enable_events=True, k=key + "-BUTTON-"),
                        sg.T(title, enable_events=True, key=key + "-TITLE-"),
                    ],
                    [sg.pin(sg.Column(layout, key=key, visible=not collapsed, metadata=arrows))],
                ],
                pad=(0, 0),
            )

        title = [sg.Text("Flyff Vision Healer", font="Any 18")]

        actions = [
            sg.Frame(
                "Actions:",
                [
                    [
                        sg.Button("Attach Window", key="-ATTACH_WINDOW-"),
                        sg.Button("Start", disabled=True, key="-START_BOT-"),
                        sg.Button("Stop (Alt+s)", disabled=True, key="-STOP_BOT-"),
                        sg.Button("Exit"),
                    ],
                    [
                        sg.Text("Attached window: ", font="Any 8", pad=((5, 0), (0, 0))),
                        sg.Text("", font="Any 8", text_color="red", key="-ATTACHED_WINDOW-", pad=(0, 0)),
                    ],
                ],
                pad=((5, 15), (0, 5)),
                size=(290, 70),
            )
        ]
        bot_options = [
            sg.Frame(
                "Options:",
                [
                    [sg.Checkbox("Show bot's vision", False, enable_events=True, key="-SHOW_FRAMES-")],
                    [
                        sg.pin(
                            sg.Checkbox(
                                "Show matches text",
                                False,
                                visible=False,
                                enable_events=True,
                                key="-SHOW_MATCHES_TEXT-",
                            )
                        )
                    ],
                    [
                        sg.pin(
                            sg.Checkbox("Show signal boxes", False, visible=False, enable_events=True, key="-SHOW_BOXES-")
                        )
                    ],
                    [
                        sg.pin(
                            sg.Checkbox(
                                "Show signal markers", False, visible=False, enable_events=True, key="-SHOW_MARKERS-"
                            )
                        )
                    ],
                    [sg.HorizontalSeparator()],
                    [sg.Text("Signal Match Threshold:")],
                    [
                        sg.Slider(
                            (0.1, 0.9),
                            0.9,
                            0.05,
                            enable_events=True,
                            orientation="h",
                            size=(20, 15),
                            key="-SIGNAL_MATCH_THRESHOLD-",
                        )
                    ],
                    [sg.Text("Healing Interval (ms):")],
                    [
                        sg.InputText("10", size=(10, 1), enable_events=True, key="-HEALING_INTERVAL_MS-"),
                    ],
                ],
                pad=((5, 15), (5, 5)),
                expand_x=True,
            )
        ]
        bot_status = [
            sg.Frame(
                "Status:",
                [
                    [sg.Text("Video FPS:", size=(15, 1), key="-VIDEO_FPS-")],
                    [sg.Multiline(size=(35, 10), key="-ML-", autoscroll=True, expand_x=True)],
                ],
                pad=((5, 15), (5, 10)),
                expand_x=True,
            )
        ]
        main = sg.Column(
            [
                actions,
                bot_options,
                bot_status,
            ],
            pad=(0, 0),
            size=(300, 500),
            scrollable=True,
            vertical_scroll_only=True,
            expand_y=True,
            key="-MAIN_COLUMN-",
        )

        video = sg.Column(
            [
                [
                    sg.pin(
                        sg.Frame(
                            "Bot's Vision:",
                            [
                                [
                                    sg.Text("Image Resolution:"),
                                    sg.Combo(
                                        list(self.frame_resolutions.keys()),
                                        default_value="400x300",
                                        key="-DEBUG_IMG_WIDTH-",
                                    ),
                                ],
                                [sg.Image(filename="", key="-DEBUG_IMAGE-")],
                            ],
                            visible=False,
                            key="-VISION_FRAME-",
                        )
                    )
                ]
            ],
            pad=(0, 0),
        )

        return [title, [main, video]]

    def __attach_window_popup(self):
        handlers = get_window_handlers()
        popup_window = sg.Window(
            "Attach Window",
            [
                [sg.Text("Please select the window to attach to:")],
                [sg.DropDown(list(handlers.keys()), key="-DROP-"), sg.Button("Refresh")],
                [sg.OK(), sg.Cancel()],
            ],
            size=(400, 100),
        )
        while True:
            event, values = popup_window.read()
            if event == "Refresh":
                handlers = get_window_handlers()
                popup_window["-DROP-"].update(values=list(handlers.keys()))
            if event in (sg.WIN_CLOSED, "Cancel"):
                popup_window.close()
                return None, None
            if event == "OK":
                popup_window.close()
                return values["-DROP-"], handlers[values["-DROP-"]]