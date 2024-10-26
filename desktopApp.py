import time

import webview
from whisper_live.client import TranscriptionClient
from whisper_live.server import TranscriptionServer
import threading
import pyautogui


class InitServerAndClient:
    def __init__(self):
        self.client_thread = None
        self.message = None
        self.client = None
        self.server_thread = None
        self.server = None

    def run_server(self, port, backend, faster_whisper_custom_model_path, whisper_tensorrt_path,
                   trt_multilingual, single_model):
        print('server running')
        faster_whisper_custom_model_path = None if faster_whisper_custom_model_path == 'None' else faster_whisper_custom_model_path
        whisper_tensorrt_path = None if whisper_tensorrt_path == 'None' else whisper_tensorrt_path
        trt_multilingual = True if trt_multilingual == 'True' else False
        single_model = True if single_model == 'True' else False
        self.server = TranscriptionServer()
        self.server_thread = threading.Thread(target=self.server.run(
            "0.0.0.0",
            int(port),
            backend, faster_whisper_custom_model_path, whisper_tensorrt_path, trt_multilingual, single_model
        ), args=("server thread", 1))
        self.server_thread.daemon = True
        self.server_thread.start()

    def run_client(self, port=9090, lang='zh'):
        self.client = TranscriptionClient(
            "localhost",
            port=int(port),
            lang=lang,
            translate=False,
            model="small",
            use_vad=False,
            save_output_recording=True,  # Only used for microphone input, False by Default
            output_recording_filename="./output_recording.wav",  # Only used for microphone input
            msg_callback=self.set_message
        )
        self.client_thread = threading.Thread(self.client(wasapi=True), args=("client thread", 2))
        self.client_thread.daemon = True
        self.client_thread.start()

    def get_message(self):
        return self.message

    def set_message(self, msg):
        self.message = msg


def showWindow(window):
    window.show()


def hideWindow(window):
    window.hide()


def destroy(window):
    # show the window for a few seconds before destroying it:
    time.sleep(0.2)
    print('Destroying window..')
    window.destroy()
    print('Destroyed!')


def hideSubtitle():
    print(123)
    hideWindow(subtitleWindow)


def showSubtitle():
    print(123)
    showWindow(subtitleWindow)


def on_start():
    hideSubtitle()


screen_width, screen_height = pyautogui.size()
initServerAndClient = InitServerAndClient()
mainWindow = webview.create_window('Main', url='MainFrame.html', js_api=initServerAndClient)
subtitleWindow = webview.create_window('Subtitle', url='Subtitle.html', width=int(int(screen_width)*0.3),
                                       height=int(int(screen_height)*0.15),frameless=True, easy_drag=True,
                                       on_top=True,js_api=initServerAndClient)
# 分配方法
mainWindow.expose(showSubtitle)
mainWindow.expose(destroy)
subtitleWindow.expose(hideSubtitle)
# 启动窗口
webview.start(on_start, debug=True)
