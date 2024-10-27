import time

import webview
from whisper_live.client import TranscriptionClient
from whisper_live.server import TranscriptionServer
import threading
import pyautogui

import multiprocessing
import os
import time


def run_server(port, backend, faster_whisper_custom_model_path, whisper_tensorrt_path, trt_multilingual, single_model):
    """服务器运行逻辑，作为独立进程运行"""
    print('Server running...')
    server = TranscriptionServer()
    try:
        server.run(
            "0.0.0.0",
            int(port),
            backend,
            faster_whisper_custom_model_path,
            whisper_tensorrt_path,
            trt_multilingual,
            not single_model
        )
    except Exception as e:
        print(f"Server encountered an error: {e}")


def run_client(port, lang, translate, model, use_vad, save_output_recording, output_recording_filename, message_queue):
    """客户端运行逻辑，作为独立进程运行"""
    client = TranscriptionClient(
        "localhost",
        port=int(port),
        lang=lang,
        translate=translate,
        model=model,
        use_vad=use_vad,
        save_output_recording=save_output_recording,
        output_recording_filename=output_recording_filename,
        msg_callback=message_queue  # 使用消息队列传递消息
    )

    # 可以添加条件以允许优雅退出
    try:
        client(wasapi=True)
    except Exception as e:
        print(f"Client encountered an error: {e}")


class InitServerAndClient:
    def __init__(self):
        self.listen_msg_process = None
        self.client_process = None
        self.server_process = None
        self.listen_msg_flag = True

    def start_server(self, port=9090, backend='faster_whisper', faster_whisper_custom_model_path=None,
                     whisper_tensorrt_path=None,
                     trt_multilingual=False, single_model=False):
        faster_whisper_custom_model_path = None if faster_whisper_custom_model_path == 'None' else faster_whisper_custom_model_path
        whisper_tensorrt_path = None if whisper_tensorrt_path == 'None' else whisper_tensorrt_path
        trt_multilingual = trt_multilingual
        single_model = single_model
        self.server = TranscriptionServer()
        if "OMP_NUM_THREADS" not in os.environ:
            os.environ["OMP_NUM_THREADS"] = str(1)
        """启动服务器进程"""
        self.server_process = multiprocessing.Process(
            target=run_server,
            args=(
                port, backend, faster_whisper_custom_model_path, whisper_tensorrt_path, trt_multilingual, single_model),
            name='server_process',
            daemon=True
        )
        self.server_process.start()

    def start_client(self, port=9090, lang='zh', translate=False, model="small", use_vad=False,
                     save_output_recording=True,
                     output_recording_filename="./output_recording.wav", ):
        """启动客户端进程"""
        self.client_process = multiprocessing.Process(
            target=run_client,
            args=(int(port), lang, translate, model, use_vad, save_output_recording, output_recording_filename,
                  message_queue),
            name='client_process',
            daemon=True
        )
        self.client_process.start()

    def listen_msg(self):
        element = subtitleWindow.dom.get_element('#subtitle')
        threading.Thread(target=self.get_msg, args=(element,), daemon=True, name="listen_msg thread").start()

    def get_msg(self, element):
        print("开始监听消息")
        while self.listen_msg_flag:
            try:
                # 尝试获取消息
                message = message_queue.get_nowait()
                print(f"Consuming: {message}")
                if message is not None:
                    print("消息" + message)
                    element.text = message
            except _queue.Empty:
                # 如果队列为空，暂停一段时间以避免过度占用CPU
                time.sleep(0.5)

    def set_listen_msg_flag(self, isTrue):
        self.listen_msg_flag = isTrue

    def stopServer(self):
        self.server_process.terminate()

    def stopClient(self):
        self.client_process.terminate()


def showWindow(window):
    window.show()


def hideWindow(window):
    window.hide()



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
