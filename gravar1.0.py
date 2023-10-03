# Importe as bibliotecas necessárias
import pyaudio  # Biblioteca para lidar com gravação de áudio em tempo real
import wave     # Biblioteca para salvar arquivos de áudio no formato WAV
import threading  # Biblioteca para executar tarefas em segundo plano
import sys       # Biblioteca para interagir com o sistema operacional

# Função para gravar áudio em segundo plano
def record_audio(frames):
    while not exit_flag.is_set():  # Enquanto não for dito para parar:
        try:
            data = stream.read(CHUNK)  # Lê um pedaço de som do microfone
            frames.append(data)       # Armazena esse pedaço de som na memória
        except IOError:
            pass  # Ignora erros

# Função para parar a gravação e salvar o arquivo
def stop_recording(frames):
    print("Pressione Enter para parar a gravação...")
    sys.stdin.read(1)  # Aguarda pressionar a tecla Enter
    exit_flag.set()    # Indica que a gravação deve parar
    stream.stop_stream()  # Para de capturar áudio do microfone
    stream.close()       # Fecha o dispositivo de captura de áudio
    audio.terminate()    # Encerra o programa que está capturando áudio
    with wave.open(OUTPUT_FILENAME, 'wb') as wf: # Abre um arquivo WAV para escrita binária com o nome especificado 
        # em OUTPUT_FILENAME.
        # O uso de "with" garante que o arquivo será fechado automaticamente após a conclusão.
        wf.setnchannels(CHANNELS) # Define o número de canais de áudio no arquivo WAV
        wf.setsampwidth(audio.get_sample_size(FORMAT)) # Configura a largura da amostra de áudio em bytes, com base no formato de áudio escolhido.
        # Aqui, estaremos usando 16b its
        wf.setframerate(RATE) # Configura a largura da amostra de áudio em bytes, com base no formato de áudio escolhido.
        wf.writeframes(b''.join(frames))  # Salva os pedaços de som como um arquivo WAV
    print("Gravação concluída. O arquivo foi salvo como:", OUTPUT_FILENAME)

# Solicita um nome para o arquivo de saída
nomegravacao = input("Insira um nome para seu arquivo (sem espaços, vírgulas, acentos ou cedilha): ")

# Configurações de gravação
FORMAT = pyaudio.paInt16  # Configura o formato de gravação para áudio de 16 bits
CHANNELS = 1             # Configura para gravar áudio mono (um canal)
RATE = 44100             # Configura a taxa de amostragem para 44100 Hz (padrão para áudio de CD)
CHUNK = 1024             # Define o tamanho de cada pedaço de áudio lido a cada vez
OUTPUT_FILENAME = nomegravacao + (".wav")  # Define o nome do arquivo de saída no formato WAV

# Inicializa a biblioteca PyAudio
audio = pyaudio.PyAudio()

# Abre um dispositivo de áudio para captura
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Cria uma sinalização para controlar a gravação
exit_flag = threading.Event()
frames = []

# Inicia a gravação em segundo plano em uma thread separada
print("Gravando... Pressione Enter para parar a gravação.")
record_thread = threading.Thread(target=record_audio, args=(frames,))
record_thread.start()

# Chama a função para parar a gravação e salvar o arquivo quando o usuário pressionar Enter
stop_recording(frames)
