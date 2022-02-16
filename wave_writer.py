#!/usr/bin/env python
import click
import csv
import numpy as np

# sfrom numpy import array
from pathlib import Path

from scipy.io import wavfile


def write_beep(file_name: Path, duration=5.0):
    f = 440  # sine frequency, Hz, may be float
    fs = 22050
    samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
    wavfile.write(file_name, 22050, samples)


@click.command()
@click.option(
    "--csv-name",
    default="example.csv",
    help="The name of the CSV file to be read in order to generate the WAV files",
)
@click.option(
    "--file-name-column",
    default="File Name",
    help="The name of the column that stores the expected name of the file",
)
@click.option(
    "--file-length-column",
    default="Duration",
    help="The name of the column that stores the expected duration of the file",
)
def run(csv_name, file_name_column, file_length_column):
    is_valid=True
    rows=[]

    # parse, validate, and modify the data as needed
    with open(csv_name) as csvfile:
        reader = csv.DictReader(
            csvfile,
        )
        row_number=0
        for row in reader:
            row_number+=1

            row[file_name_column] = row[file_name_column].strip()

            try:
                row[file_length_column] = float(row[file_length_column])
                rows.append(row)
            except:
                print(f'Row number {row_number} has an invalid value. Duration column contains {row[file_length_column]}.')
                is_valid = False
                break

    # then, use the data
    if is_valid == True:
        for row in rows:
            file_name = row[file_name_column]
            duration = row[file_length_column]
            print(f"writing {duration} s to {file_name}")
            write_beep(file_name=file_name, duration=duration)


if __name__ == "__main__":
    run()
