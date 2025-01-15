import speech_recognition as sr
import os
import pyttsx3
import webbrowser
import socket

# Inicializando o reconhecedor de fala e a síntese de fala
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def falar(texto):
    engine.say(texto)
    engine.runAndWait()

def executar_comando(comando):
    if 'Abrir navegador' in comando:
        falar("Abrindo o navegador.")
        webbrowser.open('https://www.google.com')
    elif 'fechar' in comando:
        falar("Fechando o programa.")
        os.system('taskkill /f /im programa.exe')  # Exemplo para fechar um programa
    else:
        falar("Desculpe, não entendi o comando.")

def verificar_conexao_internet():
    try:
        # Tentativa de conexão com um servidor público
        socket.create_connection(("www.google.com", 80), timeout=5)
        return True
    except (socket.timeout, socket.gaierror):
        return False

while True:
    with sr.Microphone() as source:
        print("Diga algo:")
        audio = recognizer.listen(source)

        try:
            if verificar_conexao_internet():
                # Usando o serviço online se houver conexão com a internet
                comando = recognizer.recognize_google(audio, language='pt-BR')
            else:
                # Usando o serviço offline (pocketsphinx) se não houver conexão com a internet
                comando = recognizer.recognize_sphinx(audio, language='pt-BR')

            print("Você disse: " + comando)
            executar_comando(comando)

        except sr.UnknownValueError:
            print("Não entendi.")
        except sr.RequestError:
            print("Erro de conexão com o serviço de reconhecimento de fala.")
