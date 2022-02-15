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
    help="Type the file name of the csv file, please",
)
@click.option(
    "--file-name-column",
    default=0,
    help="Write the column number with the file names",
)
@click.option(
    "--file-length-column",
    default=1,
    help="Write the column number with the file lengths",
)
def run(csv_name, file_name_column, file_length_column):
    row_number=0
    is_valid=True
    rows=[]
    with open(csv_name) as csvfile:
        reader = csv.reader(
            csvfile,
        )
        for row in reader:
            row_number+=1
            if type(row[file_name_column]) != str:
                print(f'Row number {row_number} has a wrong type. File name column contains {row[file_name_column]}.')
                is_valid = False
                break
            try:
                float(row[file_length_column])
                rows.append(row)
            except:
                print(f'Row number {row_number} has a wrong type. Length column contains {row[file_length_column]}.')
                is_valid = False
                break  
    if is_valid == True:
        for row in rows:
            file_name = row[file_name_column].strip()
            duration = float(row[file_length_column])
            print(f"writing {duration} s to {file_name}")
            write_beep(file_name=file_name, duration=duration)


if __name__ == "__main__":
    run()
