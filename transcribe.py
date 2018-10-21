import time
import IPython
import pyaudio
import wave
from rev_ai.speechrec import RevSpeechAPI

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output3.wav"

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

def await_transcript(client, id_):
    while client.view_job(id_)['status'] == 'in_progress':
        print('waiting...')
        time.sleep(1)
    return client.get_transcript(id_)


client = RevSpeechAPI('01konRYtNYr3vh5dpb_7aBXVX-IlWa9K9qhwpgMozD3YCaif9I-ioN5UkUKtrsqYQlgBCejUevifAYPIaQxuP2OnpEkrk')

print(client.get_account())
result = client.submit_job_local_file("/Users/michaelshen/Desktop/output3.wav")

transcript = await_transcript(client, result['id'])

print(transcript['monologues'][0]['elements'][:10])
IPython.embed()