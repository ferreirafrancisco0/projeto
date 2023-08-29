import sounddevice as sd
import numpy as np
import tkinter as tk
from tkinter import messagebox
import threading
import wave

class GravadorAudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gravador de Áudio")

        self.esta_gravando = False
        self.nome_arquivo = ""

        self.rotulo = tk.Label(root, text="Digite o nome do arquivo:")
        self.rotulo.pack()

        self.entrada_nome_arquivo = tk.Entry(root)
        self.entrada_nome_arquivo.pack()

        self.botao_gravar = tk.Button(root, text="Gravar", command=self.alterna_gravacao)
        self.botao_gravar.pack()

    def alterna_gravacao(self):
        if not self.esta_gravando:
            self.nome_arquivo = self.entrada_nome_arquivo.get()
            if self.nome_arquivo:
                self.esta_gravando = True
                self.botao_gravar.config(text="Parar Gravação")
                self.thread_gravacao = threading.Thread(target=self.gravar_audio)
                self.thread_gravacao.start()
            else:
                messagebox.showerror("Erro", "Digite um nome de arquivo válido.")
        else:
            self.esta_gravando = False
            self.botao_gravar.config(text="Gravar")
    
    def gravar_audio(self):
        frequencia = 26000
        duracao = 5
        ganho_gravacao = 0.5  # Ajuste o ganho conforme necessário
        frames = []

        while self.esta_gravando:
            gravacao = sd.rec(int(duracao * frequencia), samplerate=frequencia, channels=2, dtype=np.float32)
            sd.wait()
            gravacao *= ganho_gravacao  # Aplicar ganho ao áudio gravado
            frames.append(gravacao)
        
        audio_gravado = np.concatenate(frames, axis=0)
        audio_normalizado = self.normalizar_audio(audio_gravado)
        self.salvar_arquivo_wav(audio_normalizado)
    
    def normalizar_audio(self, audio):
        audio = audio / np.max(np.abs(audio))
        return audio
    
    def salvar_arquivo_wav(self, audio):
        with wave.open(self.nome_arquivo + ".wav", "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(26000)  # Ajuste a taxa de amostragem conforme necessário
            wf.writeframes(audio.tobytes())

root = tk.Tk()
app = GravadorAudioApp(root)
root.mainloop()
