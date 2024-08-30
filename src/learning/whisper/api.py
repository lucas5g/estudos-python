# Importa as bibliotecas necessárias
from flask import Flask, request, jsonify
import os
import speech_recognition as sr
import moviepy.editor as mp

app = Flask(__name__)

def video_to_text(file):
    r = sr.Recognizer()
    
    print(file)
    video = mp.VideoFileClip(file)

    audio = video.audio

    audio.write_audiofile("audio.wav")

    audio = sr.AudioFile("audio.wav")
    with audio as source:
        audio_data = r.record(source)
        texto = r.recognize_google(audio_data, language="pt-BR")

    return texto

@app.get('/')
def home():
    return {"api": "Api test transcrição"}

@app.route('/transcrever', methods=['POST'])
def upload_file():
   
    # Obtém o arquivo enviado
    arquivo = request.files['file']
    
    arquivo.save('files/'+arquivo.filename)

    
    text = video_to_text(arquivo.filename)
    return {"text": text}

  