import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Arquivos WAV", "*.wav")])
    if file_path:
        convert_audio_to_text(file_path)

def convert_audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language='pt-BR')
        print("Texto reconhecido:")
        print(text)
    except sr.UnknownValueError:
        print("Não foi possível entender o áudio")
    except sr.RequestError as e:
        print(f"Erro na solicitação: {str(e)}")


root = tk.Tk()
root.withdraw() 

file_path = filedialog.askopenfilename(filetypes=[("Arquivos WAV", "*.wav")])

if file_path:
    convert_audio_to_text(file_path)
