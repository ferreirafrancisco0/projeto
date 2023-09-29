import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import speech_recognition as sr

def convert_audio_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language='pt-BR')
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, text)
    except sr.UnknownValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Não foi possível entender o áudio")
    except sr.RequestError as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Erro na solicitação: {str(e)}")

def on_drop(event):
    file_path = event.data
    if file_path:
        convert_audio_to_text(file_path)

root = TkinterDnD.Tk()
root.title('Conversor de Áudio para Texto')

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

label = tk.Label(frame, text="Arraste e solte um arquivo WAV aqui ou clique para selecionar:")
label.pack(pady=10)

result_text = tk.Text(frame, wrap=tk.WORD, height=5, width=50)
result_text.pack(pady=10)

# Personalizar a aparência
label.config(font=('Helvetica', 12))
result_text.config(font=('Helvetica', 12))

# Cor de fundo personalizada para o widget de resultado
result_text.configure(bg='#f0f0f0')

# Cor de fundo personalizada para o frame
frame.configure(bg='#f0f0f0')

# Cor de fundo personalizada para o botão de seleção de arquivo
select_button = tk.Button(frame, text="Selecionar Arquivo", command=lambda: browse_file())
select_button.pack(pady=10)
select_button.configure(bg='#007acc', fg='white', font=('Helvetica', 12))

def browse_file():
    options = {"filetypes": [("Arquivos WAV", "*.wav")]}
    file_path = tk.filedialog.askopenfilename(**options)
    if file_path:
        convert_audio_to_text(file_path)

# Permitir que o widget Text aceite drop de arquivos
result_text.drop_target_register(DND_FILES)
result_text.dnd_bind('<<Drop>>', on_drop)

root.mainloop()
