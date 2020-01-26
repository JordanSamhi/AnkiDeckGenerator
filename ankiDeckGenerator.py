#!/usr/bin/python3

import argparse
import genanki
import hashlib
import sys


def parseArgs():
    parser = argparse.ArgumentParser(description="Generate an Anki deck from "
                                     "a file in which questions and answers "
                                     "are separated by a custom separator")

    parser.add_argument("--file", "-f", help="Name of the input file", required=True)
    parser.add_argument("--separator", "-s", help="Question/Answer \
                        separator", required=True)
    parser.add_argument("--name", "-n", help="Name of the generated deck")
    parser.add_argument("--verbose", "-v", help="Print more information",
                        action='store_true')
    parser.add_argument("--output", "-o", help="Name of the ouput file")

    return parser.parse_args()


def printError(string):
    print("[!] {}".format(string), file=sys.stderr)


def printSuccess(string):
    print("[*] {}".format(string))


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


def printVerbose(verbose, string):
    if verbose:
        printSuccess(string)


def main(args):

    filePath = args.file
    separator = args.separator
    deckName = "Default Deck"
    printVerbose(args.verbose, "Separator is: <{}>".format(separator))
    outputFile = "deck.apkg"
    if args.output:
        outputFile = args.output
    if args.name:
        deckName = args.name
    printVerbose(args.verbose, "Deckname is: {}".format(deckName))
    printVerbose(args.verbose, "output file is: {}".format(outputFile))
    printVerbose(args.verbose, "Input file is: {}".format(filePath))

    deck = genanki.Deck(
            getID(deckName),
            deckName)

    try:
        with open(filePath) as f:
            printVerbose(args.verbose, "Parsing file: {}".format(filePath))
            for line in f:
                line = line.rstrip("\n")
                printVerbose(args.verbose, "Parsing line: {}".format(line))
                split = line.split(separator)
                if len(split) != 2:
                    printError("Skipping line: <{}> due to separator problem"
                               .format(line))
                    printError("Expected format: <QUESTION>SEPARATOR<ANSWER>")
                    continue
                question = split[0]
                answer = split[1]

                note = genanki.Note(
                        model=getModel(),
                        fields=[question, answer])
                deck.add_note(note)
                printVerbose(args.verbose, "Card successfully added: \n"
                             "    Question: {} \n"
                             "    Answer: {}".format(question, answer))
            try:
                genanki.Package(deck).write_to_file(outputFile)
                printSuccess("Deck successfully created.")
                printVerbose(args.verbose, "File {} successfully written".format(outputFile))
            except IOError:
                printError("A problem occured while creating "
                           "file: {}".format(outputFile))
                printError("Aborting.")
    except IOError:
        printError("A problem occured while opening the "
                   "file: {}".format(filePath))
        printError("Aborting.")


if __name__ == "__main__":
    main(parseArgs())
