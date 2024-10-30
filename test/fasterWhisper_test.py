import librosa
from faster_whisper import WhisperModel
import soundcard as sc
import soundfile as sf
import numpy as np
import  torch
#print(torch.cuda.is_available())
model_size = "tiny"

sysmc=sc.get_microphone(id=sc.default_speaker().id,include_loopback=True)
fcNumpy=sysmc.record(48000*0.2,48000)
sf.write("t.wav",fcNumpy,samplerate=48000)
print(fcNumpy.shape)
if len(fcNumpy.shape) == 3:
    # Convert stereo to mono by averaging across channels
    audio_data_mono = np.mean(fcNumpy, axis=1)
else:
    audio_data_mono = fcNumpy  # Audio is already mono
resampled_data = librosa.resample(audio_data_mono, orig_sr=48000, target_sr=16000)
print(resampled_data.shape)
print(resampled_data)
# Run on GPU with FP16
model = WhisperModel("tiny",download_root="./model",device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
# model = WhisperModel(model_size, device="cpu", compute_type="int8")

segments, info = model.transcribe(resampled_data, beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))