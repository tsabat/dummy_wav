#!/bin/bash -ex

# installs wave_writer
pyinstaller --paths ~/.pyenv/versions/seconds/lib/python3.10/site-packages wave_writer.py
