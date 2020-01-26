#!/usr/bin/python3

import argparse
import genanki
import hashlib
import sys


def parseArgs():
    parser = argparse.ArgumentParser(description="Generate an Anki deck from \
                                     a file in which questions and answers \
                                     are separated by a custom separator")

    parser.add_argument("--file", "-f", help="Set input file", required=True)
    parser.add_argument("--separator", "-s", help="Question/Answer \
                        separator to use.", required=True)
    parser.add_argument("--name", "-n", help="Name of the generated deck.")

    return parser.parse_args()


def getID(string):
    return int(hashlib.sha256(string.encode("utf-8")).hexdigest()[:12],
               base=16)


def getModel():

    MODEL_NAME = "MODEL"

    css = ".card {\
        font-family: arial; \
            font-size: 30px; \
            text-align: center; \
            color: black; \
            background-color: white; \
        }"

    model = genanki.Model(
                getID(MODEL_NAME),
                MODEL_NAME,
                fields=[
                    {"name": "Question"},
                    {"name": "Answer"}
                ],
                templates=[
                    {
                        "name": "Card 1",
                        "qfmt": "<center>{{Question}}</center>",
                        "afmt": "<center>{{FrontSide}}<hr \
                                id=\"answer\">{{Answer}}</center>"
                    }
                ],
                css=css
            )
    return model


def main(args):

    filePath = args.file
    separator = args.separator
    deckName = "Default Deck"
    if args.name:
        deckName = args.name

    deck = genanki.Deck(
            getID(deckName),
            deckName)

    try:
        with open(filePath) as f:
            for line in f:
                line = line.rstrip("\n")
                split = line.split(separator)
                if len(split) != 2:
                    print("Skipping line: <{}> due to separator problem"
                          .format(line), file=sys.stderr)
                    print("Expected format: <QUESTION>SEPARATOR<ANSWER>", file=sys.stderr)
                question = split[0]
                answer = split[1]

                note = genanki.Note(
                        model=getModel(),
                        fields=[question, answer])
                deck.add_note(note)
                genanki.Package(deck).write_to_file("misc.apkg")
    except IOError:
        print("A problem occurend while opening the "
              "file: {}".format(filePath), file=sys.stderr)


if __name__ == "__main__":
    main(parseArgs())
