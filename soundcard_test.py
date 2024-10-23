import soundcard as sc
import soundfile as sf

OUTPUT_FILE_NAME = "out.wav"    # output file name.
SAMPLE_RATE = 48000              # [Hz]. sampling rate.
RECORD_SEC = 5000                  # [sec]. recording duration.
#data=sc.get_microphone(id=str(sc.default_speaker().name), include_loopback=True).record(SAMPLE_RATE*5,SAMPLE_RATE)
#print(data)
#sf.write(file=OUTPUT_FILE_NAME,data=data,samplerate=SAMPLE_RATE)
with sc.get_microphone(id=str(sc.default_microphone().name), include_loopback=False).recorder(samplerate=SAMPLE_RATE) as mic:
        data = mic.record(numframes=SAMPLE_RATE*5)
        print(data[:,0])
        sf.write(file=OUTPUT_FILE_NAME, data=data, samplerate=SAMPLE_RATE)