#!/usr/bin/env python
# based on : www.daniweb.com/code/snippet263775.html
from email.policy import default
import click
import math
import wave
import struct
import csv

# sfrom numpy import array
from pathlib import Path

# Audio will contain a long list of samples (i.e. floating point numbers describing the
# waveform).  If you were working with a very long sound you'd want to stream this to
# disk instead of buffering it all in memory list this.  But most sounds will fit in
# memory.
sample_rate = 44100.0


def append_silence(audio: list, duration_milliseconds=500):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(0.0)

    return


def append_sinewave(audio: list, freq=440.0, duration_milliseconds=500, volume=1.0):
    """
    The sine wave generated here is the standard beep.  If you want something
    more aggresive you could try a square or saw tooth waveform.   Though there
    are some rather complicated issues with making high quality square and
    sawtooth waves... which we won't address here :)
    """

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        audio.append(volume * math.sin(2 * math.pi * freq * (x / sample_rate)))

    return


def save_wav(audio: list, file_name):
    # Open up a wav file
    wav_file = wave.open(file_name, "w")

    # wav params
    nchannels = 1

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The stanard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        wav_file.writeframes(struct.pack("h", int(sample * 32767.0)))

    wav_file.close()

    return


def write_beep(file_name: Path, duration_milliseconds=1000):
    audio = []
    append_sinewave(audio, duration_milliseconds=duration_milliseconds)
    save_wav(audio, file_name=file_name)


@click.command()
@click.option(
    "--csv-name",
    default="example.csv",
    help="Type the file name of the csv file, please",
)
@click.option(
    "--file_name_row",
    default=0,
    help="Write the row number with the file names",
)
@click.option(
    "--file_length_row",
    default=1,
    help="Write the row number with the file lengths",
)
def run(csv_name, file_name_row, file_length_row):
    with open(csv_name) as csvfile:
        reader = csv.reader(
            csvfile,
        )
        for row in reader:
            file_name = row[file_name_row]
            duration_ms = int(float(row[file_length_row]) * 1000)
            print(f"writing {duration_ms} ms to {file_name}")
            write_beep(file_name=file_name, duration_milliseconds=duration_ms)


if __name__ == "__main__":
    run()
