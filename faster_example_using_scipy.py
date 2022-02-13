import numpy as np
from scipy.io import wavfile

file_name = "demo.wav"

duration = 90.9  # in seconds, may be float
f = 440  # sine frequency, Hz, may be float
fs = 22050
samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
wavfile.write(file_name, 22050, samples)
