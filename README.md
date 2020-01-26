# Anki Deck Generator

This tool allows one to generate an Anki deck by providing a file where:
1. Each line correspond to a question with its answer
2. Each question and answer are separated by a common separator

Medias are not taken into account yet.

## Prerequisites

```
genanki, argparse, hashlib 
```

## Usage

```
usage: ankiDeckGenerator.py [-h] --file FILE --separator SEPARATOR
                            [--name NAME] [--verbose] [--output OUTPUT]

Generate an Anki deck from a file in which questions and answers are separated
by a custom separator

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Name of the input file
  --separator SEPARATOR, -s SEPARATOR
                        Question/Answer separator
  --name NAME, -n NAME  Name of the generated deck
  --verbose, -v         Print more information
  --output OUTPUT, -o OUTPUT
                        Name of the ouput file
```

## Example of usage

```bash
./ankiDeckGenerator.py -f <INPUT_FILE> -s , -n <DECK_NAME> -o <OUTPUT_FILE>
./ankiDeckGenerator.py -f <INPUT_FILE> -s , -n <DECK_NAME>
./ankiDeckGenerator.py -f <INPUT_FILE> -s : -n <DECK_NAME> -o <OUTPUT_FILE> -v
./ankiDeckGenerator.py -f <INPUT_FILE> -s %
```

Once the output file is generated, one just has to import it in the Anki app.


:warning: genanki uses id numbers for identifying decks.
In Anki Deck Generator they are computed with the name of the Deck provided.
If the name is the same, the id will be the same.
Therefore, importing a deck with a similar name as one created with this tool will result in
updating the first deck.
It is convenient if one wants to keeps its deck statistics and add/remove some cards in a deck.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
