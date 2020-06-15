from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
import librosa
import textProcessing
import getData
import musicProcessing
import synthesis
from datetime import datetime

import os
import sys

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
@app.route('/index')

def hello():
    return render_template('start.html', title='Home')

@app.route('/again')
def again():
    return render_template('start.html', title='Home')

@app.route('/return_files')
def return_files():
    filename = 'test.wav'
    return send_file('static/output.wav',attachment_filename=filename,as_attachment=True,cache_timeout=1)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    start_time = datetime.now()
    print(start_time)
    # получаем данные из форм
    text = request.form['text']
    temp = int(request.form['temp'])

    # передаем текст в функцию, которая его распарсит и вернет список слов
    words, tokensCount = textProcessing.parseText(text)
    print(words)

    # тут мы должны вызвать функцию, которая по списку слов найдет соответствующие им аудиофайлы и вернёт их список
    melody, found_words = getData.findMelody(words)
    print(found_words)
    # обрабатываем аудиофайлы, возвращаем список сигналов
    y = musicProcessing.musicProc(melody, temp)

    if len(y) >= 2:
        # синтезируем произведение
        y_music = synthesis.synthesis(y, temp)
        librosa.output.write_wav("static/output.wav", y_music, sr=22050)

        uniqueWords = len(words)
        # print(melody)
        print(datetime.now() - start_time)
        return render_template('index.html', title='Home', tokens=words, text=text, tokensCount=uniqueWords, uniqueWords=uniqueWords)
    else:
        print(datetime.now() - start_time)
        return render_template('error.html', title='Error')

    # uniqueWords = len(words)
    # # print(melody)
    # return render_template('index.html', title='Home', tokens=words, text=text, tokensCount=uniqueWords,
    #                        uniqueWords=uniqueWords)

if __name__ == "__main__":
    app.run()



