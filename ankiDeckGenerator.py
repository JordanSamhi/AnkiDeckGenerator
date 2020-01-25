#!/usr/bin/python3

import argparse
import genanki

parser = argparse.ArgumentParser(description="Generate an Anki deck from a \
                                 file in which questions and answers are \
                                 separated by a '#'.")
parser.add_argument("--file", "-f", help="set input file", required=True)
args = parser.parse_args()

filePath = args.file

try:
    with open(filePath) as f:
        for line in f:
            split = line.split('#')
            question = split[0]
            answer = split[1]
except IOError:
    print("A problem occurend while opening the file: {}".format(filePath))
