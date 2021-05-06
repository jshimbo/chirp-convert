#!/usr/bin/python3

# Convert SARES Frequency List from Excel to
# Chirp-compatible CSV file.
#
# By Jeff AK6TG
# Version 0.1
# May 2021

from openpyxl import load_workbook
import re
import csv

# Case insensitive regular expression for "hz"
re_hertz = re.compile(re.escape('hz'), re.IGNORECASE)
# Assume frequencies always have a decimal point, e.g., 145.0
re_decimal_num = re.compile(r'\d+\.\d*')

# https://stackoverflow.com/questions/19859282/
def hasNumber(inputString):
    return any(char.isdigit() for char in inputString)


def process_name(name):
    if not name:
        return ''

    # Shorten name to fit
    answer = name.replace('Cnty ', '').replace('County ', '').upper().strip()
    # UV-R5 allow only six chars
    if len(answer) > 6:
        answer = answer.replace('-','')
    return answer

def process_comment(comment):
    if comment == None:
        answer = ''
    else:
        answer = str(comment).strip()
    return answer

def process_tone(tone):
    # Chrip defaults, if no tone
    has_tone = ''
    rToneFreq = 88.5
    cToneFreq = 88.5

    if hasNumber(tone):
        # Remove "Hz"
        # string.replace is case sensitive
        tmp_tone = float(re_hertz.sub('', tone))
        if tmp_tone > 0:
            has_tone = 'Tone'
            rToneFreq = tmp_tone

    return (has_tone, rToneFreq, cToneFreq)

def process_frequency(freq):
    found_freq = 0
    duplex = ''
    offset_freq = 0.0

    # Assumes frequency always has a decimal
    # Will output zero MHz if decimal missing
    mhz = re.match(re_decimal_num, freq)

    if mhz:
        found_freq = float(mhz.group(0))

        # Look for + or - offset
        offset = re.findall(r'\D', freq)
        if '+' in offset:
            duplex = '+'
        elif '-' in offset:
            duplex = '-'

        if duplex:
            # Offset frequency in MHz
            if found_freq > 400:
                offset_freq = 5.0
            elif found_freq > 200:
                offset_freq = 1.6
            elif found_freq > 100:
                offset_freq = 0.6

    return (found_freq, duplex, offset_freq)

def process_row(row):
    # print(row)
    freq_data = process_frequency(str(row[1]))
    tone_data = process_tone(row[2])
    name = process_name(row[3])
    comment = process_comment(row[4]) # do not convert to string
    one_row = {
        "Location": row[0],
        "Name": name,
        "Frequency": format(freq_data[0], 'f'),
        "Duplex": freq_data[1],
        "Offset": format(freq_data[2], 'f'),
        "Tone": tone_data[0],
        "rToneFreq": tone_data[1],
        "cToneFreq": tone_data[2],
        "DtcsCode": '023',
        "DtcsPolarity": 'NN',
        "Mode": 'FM',
        "TStep": '5.00',
        "Skip": '',
        "Comment": comment,
        "URCALL": '',
        "RPT1CALL": '',
        "RPT2CALL": '',
        "DVCODE": ''
    }
    return one_row

def main():
    import sys
    import os.path
    from os import path

    if len(sys.argv) < 2:
        print("Usage: {} filename".format(sys.argv[0]))
        return False

    filename = sys.argv[1]
    if not path.isfile(filename):
        print("{} is not a file".format(filename))
        return False

    wb = load_workbook(filename = sys.argv[1], data_only=True)
    ws = wb.active

    last_row = 0
    chirp_data = []
    for row in ws.values:
        if type(row[0]) == int and row[0] > last_row:
            chirp_data.append(process_row(row))
            last_row += 1

    # Close the workbook after reading
    wb.close()

    output_file = "output.csv"

    # Write dictionary to CSV file.
    # Thanks to stackoverflow
    f = open(output_file, 'w')
    c = csv.DictWriter(f, chirp_data[0].keys())
    c.writeheader()
    c.writerows(chirp_data)
    f.close()
    print("Created {}".format(output_file))

if __name__ == "__main__":
    main()
