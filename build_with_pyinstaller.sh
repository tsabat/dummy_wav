#!/bin/bash

# instsalls wave_writer
pyinstaller wave_writer.py

# moves the example to the dir to test it
cp example.csv dist/wave_writer

# run with example file
cd dist/wave_writer
./wave_writer
echo "removing test files"
rm -rf *.wav