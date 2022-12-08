*************
Chirp-Convert
*************

This Python script converts the SARES Frequency List Excel file
into a Chirp-compatible CSV file. Although, I made some
SARES-specific optimizations, a few cells must be manually
edited, e.g., the comments in channels 51-53.

The problem I'm trying to solve is the divergence between the
Excel and Chirp files, e.g., tones for simplex channels.
Now, the Excel file can be the single source of truth.

How to use the tool.

1. Install Python 3.x. In Windows, you can install Python from the Microsoft Store.

2. Install the openpyxl Python package. https://openpyxl.readthedocs.io/en/stable/

3. Run the program: ``python3 chirp_convert/main.py SARES-FreqList.xlsx``

4. Open ``output.csv`` in Excel and tweak as needed.

5. In Chirp, open a new frequency list (File -> New) and then import ``output.csv``.

6. Delete channel 0 and QA the file.

7. File -> Save As to your final Chirp file.

Done.
