import csv
import numpy as np

from pathlib import Path

from scipy.io import wavfile

WAV_EXTENSION = ".wav"


def parse_validate_and_clean(csv_name, file_name_column, file_length_column, debug):
    is_valid = True
    rows=[]
    with open(csv_name) as csvfile:
        reader = csv.DictReader(
            csvfile,
        )
        row_number=0
        seen_file_names = set()
        for row in reader:
            row_number+=1

            clean_file_name = row[file_name_column].strip()
            if not clean_file_name.endswith(WAV_EXTENSION):
                if debug:
                    print(f"Adding {WAV_EXTENSION} to {clean_file_name}")
                clean_file_name = f"{clean_file_name}{WAV_EXTENSION}"
            if clean_file_name in seen_file_names:
                print(f'Row number {row_number} has a duplicate filename, {clean_file_name}. Please rename and try again')
                is_valid = False
                break
            seen_file_names.add(clean_file_name)
            row[file_name_column] = clean_file_name

            try:
                row[file_length_column] = float(row[file_length_column])
                rows.append(row)
            except:
                print(f'Row number {row_number} has an invalid value. Duration column contains {row[file_length_column]}. Please enter a number and try again')
                is_valid = False
                break
    return is_valid, rows


def write_beeps(rows, file_name_column, file_length_column, debug):
    for row in rows:
        file_name = row[file_name_column]
        duration = row[file_length_column]
        if debug:
            print(f"Creating {file_name} with {duration} second duration")
        write_beep(file_name=file_name, duration=duration)


def write_beep(file_name: Path, duration=5.0):
    f = 440  # sine frequency, Hz, may be float
    fs = 22050
    samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
    wavfile.write(file_name, 22050, samples)