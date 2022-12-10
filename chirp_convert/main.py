#!/usr/bin/python3

# Convert SARES Frequency List from Excel to CSV for Chirp
#
# Jeff AK6TG
# Version 0.2
# Dec 2022

import argparse
import csv
import re
import sys
from os import path
from openpyxl import load_workbook


# The deicmal point is optional
re_decimal_num = re.compile(r'\d+\.?\d*')


def process_name(name, name_format):
    if not name:
        # Packet channel does not have a name
        return ''

    # defaults
    light_touch = False
    maxlen = 7
    # light_touch allows lowercase and 8 char names
    if name_format == 'loose':
        light_touch = True
        maxlen = 8  # e.g., Kenwood TH-F6
    elif name_format == 'strict':
        maxlen = 6  # e.g., FT-60r

    # Shorten name and convert to upper case
    answer = name.replace('Cnty ', '').replace('County ', '').strip()

    if not light_touch:
        # If name ends with a lowercase letter, insert a space
        # and (later) convert to uppercase
        if answer[-1:].islower():
            answer = answer[:-1] + ' ' + answer[-1:]

        # Four char names are <city code> and lowercase subchannel
        if len(answer) == 4:
            # insert a space
            answer = answer[:3] + ' ' + answer[-1:]

        # Convert all names to all CAPS by default
        # Do this last
        answer = answer.upper()  # uppercase

    # Strip hyphens to shorten name is too long
    if len(answer) > maxlen:
        answer = answer.replace('-', '')

    # If still too long, remove spaces
    if len(answer) > maxlen:
        answer = answer.replace(' ', '')

    # If still too long, print warning
    if len(answer) > maxlen:
        print("Warning: Channel name --", answer, "-- is to too long")

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

    if tone:
        s = re_decimal_num.search(tone)
        if s:
            freq = float(s.group())
            if freq > 0:
                # Tone is always positive
                has_tone = 'Tone'
                rToneFreq = freq

    return (has_tone, rToneFreq, cToneFreq)


def process_frequency(freq):
    found_freq = 0
    duplex = ''
    offset_freq = 0.0

    # Decimal is optional in re_decimal_num
    mhz = re_decimal_num.search(freq)
    if mhz:
        found_freq = float(mhz.group())

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
                if duplex == '-':
                    print("Warning: found negative offset for 440 MHz")
            elif found_freq > 200:
                offset_freq = 1.6
            elif found_freq > 100:
                offset_freq = 0.6

    return (found_freq, duplex, offset_freq)


def process_row(row, name_format):
    # print(row)
    freq_data = process_frequency(str(row[1]))
    tone_data = process_tone(row[2])
    name = process_name(row[3], name_format)
    comment = process_comment(row[4])  # it is already a string
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


def main(args):
    # format of channel names
    if args.loose and args.strict:
        print("Error: Cannot specify -l and -s. Exiting.")
        sys.exit(1)

    name_format = ''
    if args.loose:
        # allow lowercase, up to 8 chars
        name_format = 'loose'
    elif args.strict:
        name_format = 'strict'

    filename = args.filename
    if not path.isfile(filename):
        print(filename, "not found")
        sys.exit(2)

    wb = load_workbook(filename=filename, data_only=True)
    ws = wb.active

    last_row = 0
    chirp_data = []
    for row in ws.values:
        if type(row[0]) == int and row[0] > last_row:
            chirp_data.append(process_row(row, name_format))
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
    parser = argparse.ArgumentParser(
        description='Convert SARES Excel frequency list to Chirp CSV file'
    )
    parser.add_argument(
        "-l", '--loose',
        default=False,
        action='store_true',
        help="Allow lowercase and 8 characters in channel names"
    )
    parser.add_argument(
        "-s", '--strict',
        default=False,
        action='store_true',
        help="Limit channel names to six chars"
    )
    parser.add_argument("filename")
    args = parser.parse_args()
    main(args)
