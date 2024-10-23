from whisper_live.client import TranscriptionClient
client = TranscriptionClient(
"localhost",
9090,
lang="zh",
translate=False,
model="small",
use_vad=False,
save_output_recording=True, # 仅用于麦克风输入，默认为 False
output_recording_filename="./output_recording.wav", # 仅用于麦克风输入
)
client(wasapi=True)
#client()