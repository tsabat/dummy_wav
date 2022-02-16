#!/usr/bin/env python
import click

from library import parse_validate_and_clean, write_beeps


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
@click.option(
    "-d",
    "--debug",
    default=False, 
    is_flag=True,
    help="Whether or not to show debug output",
)
def run(csv_name, file_name_column, file_length_column, debug):
    is_valid, rows = parse_validate_and_clean(csv_name, file_name_column, file_length_column, debug)

    # then, use the data
    if is_valid == True:
        write_beeps(rows, file_name_column, file_length_column, debug)


if __name__ == "__main__":
    run()
