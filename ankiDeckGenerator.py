#!/usr/bin/python3

import argparse
import genanki

parser = argparse.ArgumentParser(description="Generate an Anki deck from a \
                                 file in which questions and answers are \
                                 separated by a '#'.")
parser.add_argument("--file", "-f", help="set input file", required=True)
args = parser.parse_args()

filePath = args.file

model = genanki.Model(
            9318570375603865,
            "Model",
            fields=[
                {"name": "Question"},
                {"name": "Answer"}
            ],
            templates=[
                {
                    "name": "Card 1",
                    "qfmt": "{{Question}}",
                    "afmt": "{{FrontSide}}<hr \
                            id=\"answer\">{{Answer}}"
                }
            ]
        )

deck = genanki.Deck(
        2890547594726454,
        "Misc")

try:
    with open(filePath) as f:
        for line in f:
            split = line.split('#')
            question = split[0]
            answer = split[1]

            note = genanki.Note(
                    model=model,
                    fields=[question, answer])

            deck.add_note(note)

            genanki.Package(deck).write_to_file("misc.apkg")
except IOError:
    print("A problem occurend while opening the file: {}".format(filePath))
