import librosa.display
import numpy as np
import math

# Функция изменнения темпа мелодии
def changeTempo(y, sr, gl_tempo):
    # определяем начальный темп
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

    print("Темп до: " + str(tempo))
    # print(beats)

    # изменяем темп и пересчитываем биты
    y1 = librosa.effects.time_stretch(y, gl_tempo / tempo)
    onset_env = librosa.onset.onset_strength(y1, sr=sr, aggregate=np.median)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    print("Темп после: " + str(tempo))
    # print(beats)

    if abs(tempo - gl_tempo) < 5:
        y = y1

    return y

def computeRMS(y):
    sum = 0
    for i in range(len(y)):
        sum += y[i] * y[i]
    rms = math.sqrt(sum / len(y))
    return rms

def changeVolume(y, amp):
    # находим максимум амплитуды
    max_amp = max(y)
    # Вычисляем RMS
    # rms = computeRMS(y)
    # print(rms)
    # изменяем громкость
    for i in range(len(y)):
        y[i] *= amp/max_amp
    return y


def musicProc(files, temp):
    y = []  # временной ряд
    sr = 22050  # частота дискретизации
    vol = 0.8

    print(len(files))
    for number in range(len(files)):
        if files[number] != '':
            y_new, _ = librosa.load(files[number], sr)

            y_new = changeTempo(y_new, sr, temp)
            y_new = changeVolume(y_new, vol)

            y.append(y_new)

    return y