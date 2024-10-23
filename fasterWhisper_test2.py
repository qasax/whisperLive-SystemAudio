import librosa
from faster_whisper import WhisperModel
import soundcard as sc
import soundfile as sf
import numpy as np
import  torch
#print(torch.cuda.is_available())
model_size = "tiny"

sysmc=sc.get_microphone(id=sc.default_speaker().id,include_loopback=True)
fcNumpy=sysmc.record(16000*0.8,16000)
sf.write("t.wav",fcNumpy,samplerate=16000)
print(fcNumpy)
if len(fcNumpy.shape) == 2:
    # Convert stereo to mono by averaging across channels
    audio_data_mono = np.mean(fcNumpy, axis=1)
else:
    audio_data_mono = fcNumpy  # Audio is already mono
# Run on GPU with FP16
model = WhisperModel("tiny",download_root="./model",device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe(audio_data_mono, beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))