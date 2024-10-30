import json
import threading

from whisper_live.client import TranscriptionClient


class ScriptRunner:
    def __init__(self):
        self.output = []

    def run_script(self):
        client = TranscriptionClient(
            "localhost",
            9090,
            lang="zh",
            translate=False,
            model="small",
            use_vad=False,
            save_output_recording=True,  # 仅用于麦克风输入，默认为 False
            output_recording_filename="../desktop/output_recording.wav",  # 仅用于麦克风输入
        )
        client(wasapi=True)

    def get_output(self):
        return json.dumps(self.output)


if __name__ == "__main__":
    # window = webview.create_window('Woah dude!', 'MainFrame.html')
    runner = ScriptRunner()
    threading.Thread(target=runner.run_script, daemon=True).start()
    #sleep(1000)
    # webview.start()