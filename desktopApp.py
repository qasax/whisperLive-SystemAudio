import webview
from whisper_live.client import TranscriptionClient
from whisper_live.server import TranscriptionServer
import threading


class WebClient:
    def __init__(self):
        self.client_thread = None
        self.message = None
        self.client = None

    def run_client(self, port=9090, lang='zh'):
        self.client = TranscriptionClient(
            "localhost",
            port=port,
            lang=lang,
            translate=False,
            model="small",
            use_vad=False,
            save_output_recording=True,  # Only used for microphone input, False by Default
            output_recording_filename="./output_recording.wav" , # Only used for microphone input
            msg_callback=self.set_message
        )
        self.client_thread = threading.Thread(self.client(), args=("client thread", 2))
        self.client_thread.daemon = True
        self.client_thread.start()

    def get_message(self):
        return self.message

    def set_message(self, msg):
        self.message = msg


class WebServer:

    def __init__(self):
        self.server_thread = None
        self.server = None

    def run_server(self, port, backend, faster_whisper_custom_model_path, whisper_tensorrt_path,
                   trt_multilingual, single_model):
        self.server = TranscriptionServer()
        self.server_thread = threading.Thread(target=self.server.run(
            "0.0.0.0",
            port,
            backend,
            faster_whisper_custom_model_path,
            whisper_tensorrt_path,
            trt_multilingual,
            single_model,
        ), args=("server thread", 1))
        self.server_thread.daemon = True
        self.server_thread.start()


def showSubtitle():
    subtitleWindow.show()


def on_start():
    subtitleWindow.hide()


client = WebClient()
mainWindow = webview.create_window('', url='MainFrame.html', js_api=client)
subtitleWindow = webview.create_window('', url='MainFrame.html', frameless=True, easy_drag=True, js_api=client)
mainWindow.expose(showSubtitle)
webview.start(on_start)
