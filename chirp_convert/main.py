#!/usr/bin/python3

# Convert SARES Frequency List from Excel to CSV for Chirp
#
# Jeff AK6TG
# Version 1.0
# August 2024

import argparse
import csv
import re
import sys
from os import path
from openpyxl import load_workbook


def process_name(name, name_format):
    if not name:
        # Packet channel does not have a name
        return ""

    # defaults
    maxlen = 7
    upper_case = True

    # light_touch allows lowercase and 8 char names
    if name_format == "loose":
        upper_case = False
        maxlen = 8  # e.g., Kenwood TH-F6
    elif name_format == "strict":
        maxlen = 6  # e.g., FT-60r

    # Remove "County" from name
    answer = name.replace("Cnty ", "").replace("County ", "").strip()

    # If name ends with a lowercase letter, insert a space
    if answer[-1:].islower():
        answer = answer[:-1] + " " + answer[-1:]

    # If name is too long, remove hyphen.
    if len(answer) > maxlen:
        answer = answer.replace("-", "")

    # If still too long, remove spaces
    if len(answer) > maxlen:
        answer = answer.replace(" ", "")

    # If still too long, complain
    if len(answer) > maxlen:
        print("Warning: Channel name --", answer, "-- is to too long")

    if upper_case:
        answer = answer.upper()

    return answer


def process_comment(comment):
    if comment:
        answer = comment.strip()
    else:
        answer = ""

    return answer


def process_tone(s):
    # Chrip defaults, if no tone
    has_tone = ""
    rToneFreq = 88.5
    cToneFreq = 88.5  # We do not use this.

    re_tone = re.compile(r"(\d+\.?\d*)")

    if s:
        tone = re_tone.search(s)
        if tone:
            freq = float(tone.group(1))
            if freq > 0:
                # Tone is always positive
                has_tone = "Tone"
                rToneFreq = freq

    return (has_tone, rToneFreq, cToneFreq)


def process_frequency(s):
    found_freq = 0
    duplex = ""
    offset_freq = 0.0

    re_frequency = re.compile(r"(\d+\.?\d*)(.*)")

    # Decimal is optional in re_decimal_num
    freq = re_frequency.search(s)
    if freq:
        found_freq = float(freq.group(1))

        # Look for + or - offset
        offset = freq.group(2)
        if "+" in offset:
            duplex = "+"
        elif "-" in offset:
            duplex = "-"

        if duplex:
            # Offset frequency in MHz
            if found_freq > 400:
                offset_freq = 5.0
                if duplex == "-":
                    print(
                        "Warning: found negative offset for 440 MHz. Converting to plus."
                    )
                    duplex = "+"
            elif found_freq > 200:
                offset_freq = 1.6
            elif found_freq > 100:
                offset_freq = 0.6

    return (found_freq, duplex, offset_freq)


def process_row(row, name_format):
    freq_data = process_frequency(str(row[1]))
    tone_data = process_tone(row[2])
    name = process_name(row[3], name_format)
    comment = process_comment(row[4])
    one_row = {
        "Location": row[0],
        "Name": name,
        "Frequency": format(freq_data[0], "f"),
        "Duplex": freq_data[1],
        "Offset": format(freq_data[2], "f"),
        "Tone": tone_data[0],
        "rToneFreq": tone_data[1],
        "cToneFreq": tone_data[2],
        "DtcsCode": "023",
        "DtcsPolarity": "NN",
        "Mode": "FM",
        "TStep": "5.00",
        "Skip": "",
        "Comment": comment,
        "URCALL": "",
        "RPT1CALL": "",
        "RPT2CALL": "",
        "DVCODE": "",
    }
    return one_row


def main(args):
    # format of channel names
    if args.loose and args.strict:
        print("Error: Cannot specify both -l and -s. Exiting.")
        sys.exit(1)

    name_format = ""
    if args.loose:
        # allow lowercase, up to 8 chars
        name_format = "loose"
    elif args.strict:
        name_format = "strict"

    filename = args.filename
    if not path.isfile(filename):
        print(filename, "not found")
        sys.exit(2)

    wb = load_workbook(filename=filename, data_only=True)
    ws = wb.active

    chirp_data = []
    for row in ws.values:
        if type(row[0]) == int:
            chirp_data.append(process_row(row, name_format))

    # Close the workbook after reading
    wb.close()

    output_file = "chirp.csv"

    # Write dictionary to CSV file.
    # Thanks to stackoverflow
    f = open(output_file, "w")
    c = csv.DictWriter(f, chirp_data[0].keys())
    c.writeheader()
    c.writerows(chirp_data)
    f.close()
    print("Created {}".format(output_file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert SARES Excel frequency list to Chirp file named chirp.csv"
    )
    parser.add_argument(
        "-l",
        "--loose",
        default=False,
        action="store_true",
        help="Mixed case channel names, for Kenwood TH-F6a",
    )
    parser.add_argument(
        "-s",
        "--strict",
        default=False,
        action="store_true",
        help="Short names, for FT-60r",
    )
    parser.add_argument(
        "filename",
        nargs="?",
        default="SARES-FreqList.xlsx",
        help="Default input file is SARES-FreqList.xlsx",
    )
    args = parser.parse_args()
    main(args)
