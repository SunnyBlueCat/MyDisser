import librosa
import librosa.display
import numpy as np

import musicProcessing


def melodyAnalysis(y1, y2, temp):
    sr = 22050
    d = int(sr / (temp / 60))

    # Для первой мелодии
    onset_env = librosa.onset.onset_strength(y1, sr=sr, aggregate=np.median)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    # время последнего бита
    t1 = int(librosa.frames_to_time(beats[-1], sr=sr) * sr)
    # print(t1)
    # если мелодия не закончилась, откладываем ещё один бит
    if d < y1.size - t1:
        t1 += d
    # print(t1)

    # Для второй мелодии
    onset_env = librosa.onset.onset_strength(y2, sr=sr, aggregate=np.median)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    # Время первого бита
    t2 = int(librosa.frames_to_time(beats[0], sr=sr) * sr)
    # print(t2)
    # если перед первым битом есть ещё время, откладываем вначале ещё один бит
    if d < t2:
        t2 = d
    # print(t2)

    return t1, t2

def synthesis2melodies(y1, y2, t1, t2):
    # Соединяем мелодии
    y = np.hstack((y1[0:t1],y2[t2:]))

    # Делаем наложение мелодий
    if len(y1[0:t1]) > len(y2[0:t2]):
        for i in range(t2-1):
            y[t1 - t2 + i] += y2[i]*0.5
    if len(y1[t1:]) < len(y2[t2:]):
        for i in range(y1.size - t1):
            y[t1 + i] += y1[t1 + i]*0.5
    return y

def synthesis(y, temp):
    sr = 22050
    # попарно синтезируем мелодии
    y_new = y[0]
    for i in range(len(y)-1):
        t1, t2 = melodyAnalysis(y_new, y[i+1], temp)
        y_new = synthesis2melodies(y_new, y[i+1], t1, t2)

    y_new = librosa.effects.harmonic(y_new)
    # librosa.output.write_wav("output.wav", y_new, sr)
    return y_new


