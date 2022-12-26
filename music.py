import numpy as np
from scipy.io import wavfile
from playsound import playsound

sampleRate = 44100

t = np.linspace(0, 20, sampleRate * 5)
y = np.sin(440 * t)

wavfile.write('Sine.wav', sampleRate, y)

playsound('Sine.wav')