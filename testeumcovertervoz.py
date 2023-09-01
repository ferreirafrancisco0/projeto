import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.AudioFile('audio.wav') as source:
    
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
