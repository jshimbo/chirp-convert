# Chirp-Convert

This Python script converts the SARES Frequency List Excel file into a Chirp-compatible CSV file.

By creating the CSV file automatically, the Excel file can be the source of truth.

## Prerequisites

* Python 3
* Openpyxl Python package https://openpyxl.readthedocs.io/

## Quickstart

1. `git clone https://github.com/jshimbo/chirp-convert`
2. `cd chirp-convert`
3. `python3 -m venv .venv`
4. `. .venv/bin/activate`
5. `pip install openpyxl`
6. `python3 chirp-convert\main.py --help`
7. `python3 chirp-convert\main.py SARES-FreqList.xlsx`

### Notes

- The output file is always `output.csv`.
- Steps 3 and 4 create a Python virtual environment, as required on many operating systems.
- Channel names
  - By default, channel names are uppercase and up to seven characters long, which the BarFeng UV-5R supports.
  - If you have a Yaesu FT-60r, use the `-s` or `--strict` option.
  - If you have a Kenwood TH-F6a, use the `-l` or `--loose` option, which allows lowercase and up to eight characters.
- Open `output.csv` in a spreadsheet program and edit to taste. Remember to save to a CSV file.
- Get the SARES Frequency list from the SARES-RG Github site, https://github.com/saresrg/Go-Kit-Forms/releases/latest.


## Programming Your Radio

1. Start the Chirp program.
2. Connect your radio.
3. In Chirp, `Radio > Download from radio...` [Copy memory from radio to computer.]
4. In Chirp, `File > Import from file...` and choose your `output.csv` file. Chirp will display a scary warning but click OK to proceed. Only the SARES channel numbers will be modified.
5. Copy chananel data from your computer to your radio, `Radio > Upload to radio...`

Done.
