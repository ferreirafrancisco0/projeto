# Importar as bibliotecas necessárias
import tkinter as tk  # Biblioteca para criar interfaces gráficas
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD  # Extensões para arrastar e soltar arquivos
import speech_recognition as sr  # Biblioteca para reconhecimento de fala

# Função para converter áudio em texto
def convert_audio_to_text(audio_file):
    recognizer = sr.Recognizer()  # Inicializa um reconhecedor de fala
    with sr.AudioFile(audio_file) as source:
        recognizer.adjust_for_ambient_noise(source)  # Ajusta o reconhecimento para o ambiente
        audio = recognizer.record(source)  # Grava o áudio do arquivo

    try:
        text = recognizer.recognize_google(audio, language='pt-BR')  # Tenta reconhecer o áudio em texto
        result_text.delete(1.0, tk.END)  # Limpa o widget de texto de resultados
        result_text.insert(tk.END, text)  # Insere o texto reconhecido no widget de resultados
    except sr.UnknownValueError:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "Não foi possível entender o áudio")
    except sr.RequestError as e:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Erro na solicitação: {str(e)}")

# Função para abrir uma janela de seleção de arquivo
def browse_file():
    options = {"filetypes": [("Arquivos WAV", "*.wav")]}
    file_path = filedialog.askopenfilename(**options)
    if file_path:
        convert_audio_to_text(file_path)

# Função chamada quando um arquivo é arrastado e solto na interface
def on_drop(event):
    file_path = event.data  # Obtém o caminho do arquivo que foi solto
    if file_path:
        convert_audio_to_text(file_path)  # Chama a função para converter o áudio em texto

# Cria a janela da interface gráfica
root = TkinterDnD.Tk()
root.title('Conversor de Áudio para Texto')

# Cria um quadro (frame) na janela
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Cria uma etiqueta (label) na interface
label = tk.Label(frame, text="Arraste e solte um arquivo WAV aqui ou clique para selecionar:")
label.pack(pady=10)

# Cria um widget de texto para exibir o resultado do reconhecimento
result_text = tk.Text(frame, wrap=tk.WORD, height=5, width=50)
result_text.pack(pady=10)

# Personalização da aparência dos elementos da interface
label.config(font=('Helvetica', 12))
result_text.config(font=('Helvetica', 12))
result_text.configure(bg='#f0f0f0')  # Define a cor de fundo para o widget de resultados
frame.configure(bg='#f0f0f0')  # Define a cor de fundo para o quadro

# Cria um botão para selecionar um arquivo
select_button = tk.Button(frame, text="Selecionar Arquivo", command=browse_file)
select_button.pack(pady=10)
select_button.configure(bg='#007acc', fg='white', font=('Helvetica', 12))

# Permite que o widget de texto aceite arquivos arrastados e soltos
result_text.drop_target_register(DND_FILES)
result_text.dnd_bind('<<Drop>>', on_drop)

# Inicia a interface gráfica
root.mainloop()
