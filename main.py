import numpy as np
import wavio
import csv


def write_file(duration, name):
  rate = 22050  # samples per second
  freq = 440.0     # sound frequency (Hz)
  t = np.linspace(0, duration, duration*rate, endpoint=False)
  x = np.sin(2 * np.pi * freq * t)
  print(f"writing {name}")
  wavio.write(name, x, rate, sampwidth=3)


with open('example.csv') as csvfile:
    reader = csv.reader(csvfile, )
    for row in reader:
        write_file(row[1], row[0])
