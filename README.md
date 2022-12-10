# Chirp-Convert

This Python script converts the SARES Frequency List Excel file into a Chirp-compatible CSV file.

The problem I'm trying to solve is discrepancies that creep in between the Excel and CSV files when they are maintained separately and manually.
By creating the CSV file automatically, the Excel file can be the source of truth.

## How to Use This Tool

1. Install Python 3.x. In Windows, you can install Python from the Microsoft Store.
1. Install the openpyxl Python package. https://openpyxl.readthedocs.io/en/stable/
1. Clone this repository or download just the file `chirp_convert/main.py`.
1. Run the program: `python3 chirp_convert/main.py SARES-FreqList.xlsx`
   - The output file will be `output.csv`
   - By default, the CSV file will be appropriate for BaoFeng UV-5R (seven characters, uppercase).
   - The `-s` or `--strict` option squishes channel names to six characters, for the Yaesu FT-60
   - The `-l` or `--loose` option allows eight characters and lowercase, for the Kenwood TH-F6.
   - `python3 chirp_convert/main.py -h` also shows you the above info.
1. Open `output.csv` in a spreadsheet program and edit to taste. Remember to save to a CSV file.
1. In Chirp, open a new frequency list (File -> New) and then import `output.csv`.
1. Edit the info as needed.
1. File -> Save As to your final Chirp file.

Done.

## How to Program Your Radio

1. Start Chirp and connect to your radio.
1. Read the channel data from the radio to Chirp.
1. Import the SARES Chirp file. This overwrites only the SARES channels.
1. Review the info.
1. Write the channel data from Chirp to your radio.

Done.
