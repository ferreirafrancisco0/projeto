import pyaudio
import wave
import threading
import sys

def record_audio(frames):
    while not exit_flag.is_set():
        try:
            data = stream.read(CHUNK)
            frames.append(data)
        except IOError:
            pass

def stop_recording(frames):
    print("Pressione Enter para parar a gravação...")
    sys.stdin.read(1)
    exit_flag.set()
    stream.stop_stream()
    stream.close()
    audio.terminate()
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    print("Gravação concluída. O arquivo foi salvo como:", OUTPUT_FILENAME)

nomegravacao = input("Insira um nome para seu arquivo (sem espaços, vírgulas, acentos ou cedilha): ")

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = nomegravacao + (".wav")

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

exit_flag = threading.Event()
frames = []

print("Gravando... Pressione Enter para parar a gravação.")
record_thread = threading.Thread(target=record_audio, args=(frames,))
record_thread.start()
stop_recording(frames)
