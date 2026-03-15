#!/usr/bin/python3
"""Main program of a word guessing game."""
import argparse
import pathlib
import random
import sys


# pylint: disable-next=R0903
class UiColors:
    """Definitions of UI colors; for all details check
    https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    GREEN_BACKGROUND = '\033[30;102m'
    YELLOW_BACKGROUND = '\033[30;103m'
    GREY = '\033[30;47m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Tile:
    """Represents a tile containing a letter in the game board"""

    GREEN_BACKGROUND = '\033[30;102m'
    YELLOW_BACKGROUND = '\033[30;103m'
    GREY_BACKGROUND = '\033[30;47m'
    DARK_BACKGROUND = '\033[48;5;237m'
    END_COL = '\033[0m'

    def __init__(self, letter: str):
        self.letter = letter
        self.is_correct = None
        self.is_partially_correct = None
        self.is_wrong = None

    def __str__(self):
        return self.to_string()

    def is_unused(self):
        return self.is_correct is None and self.is_partially_correct is None and self.is_wrong is None

    def to_string(self):
        if self.is_correct:
            return f'{self.GREEN_BACKGROUND} {self.letter.upper()} {self.END_COL}'
        elif self.is_partially_correct:
            return f'{self.YELLOW_BACKGROUND} {self.letter.upper()} {self.END_COL}'
        elif self.is_wrong:
            return f'{self.DARK_BACKGROUND} {self.letter.upper()} {self.END_COL}'
        else:
            return f'{self.GREY_BACKGROUND} {self.letter.upper()} {self.END_COL}'


def blank_out_first_occurrence(word, param):
    for index, letter in enumerate(word):
        if letter == param:
            word[index] = " "
            return


class WorderGame:
    """Represents a round in the game of Worder"""

    def __init__(self, word_length):
        self.word_length = word_length
        self.dictionary = load_dictionary(word_length)
        self.alphabet = list(map(lambda letter: Tile(letter), list('abcdefghijklmnopqrstuvwxyz')))
        self.used_letters = set([])
        self.tile_rows = []
        self.guesses = []
        self.won = False

    def play(self):
        secret_word = random.choice(list(self.dictionary))
        guess_counter = 1
        while guess_counter < 7:
            guess = self.read_guess(guess_counter)
            self.guesses.append(guess)
            tile_row = []
            for index, letter in enumerate(secret_word):
                tile = Tile(guess[index])
                tile_row.append(tile)
            correct_counter = 0
            unguessed_letters = list(f'{secret_word}')
            for index, letter in enumerate(unguessed_letters):
                if guess[index] == letter:
                    correct_counter += 1
                    tile_row[index].is_correct = True
                    unguessed_letters[index] = " "
            for index, letter in enumerate(unguessed_letters):
                if guess[index] in unguessed_letters:
                    if tile_row[index].is_unused():
                        tile_row[index].is_partially_correct = True
                        blank_out_first_occurrence(unguessed_letters, guess[index])
                else:
                    tile_row[index].is_wrong = True
                    self.used_letters.add(guess[index])

            self.won = correct_counter == self.word_length
            self.tile_rows.append(tile_row)
            for tr in self.tile_rows:
                print('        |', end=' ')
                for t in tr:
                    print(t, end=' ')
                print('|')
            if self.won:
                break
            for every in self.alphabet:
                if every.letter in self.used_letters:
                    every.is_wrong = True
            for tile in tile_row:
                if tile.is_correct:
                    for every in self.alphabet:
                        if every.letter == tile.letter:
                            every.is_correct = True
                if tile.is_partially_correct:
                    for every in self.alphabet:
                        if every.letter == tile.letter:
                            every.is_partially_correct = True
            print('')
            for every in self.alphabet:
                print(f'{every} ', end='')
            print('\n')
            guess_counter += 1
        print(get_final_message(self.won, guess_counter, secret_word))

    def read_guess(self, guess_counter):
        """Read a guess from stdin"""
        while True:
            guess = input(f'Guess #{guess_counter}? ').lower()
            if len(guess) != self.word_length:
                print(f'{guess} is not a {self.word_length}-letter word. Try again.')
                continue
            if guess not in self.dictionary:
                print(f'{guess} is not in the dictionary. Try again.')
                continue
            break
        return guess


def load_dictionary(word_length):
    """Loads the word list for the given length into a set."""
    dictionary_path = pathlib.Path(__file__).parent / f'word{word_length}'
    with open(dictionary_path, encoding='utf-8') as word_file:
        return set(word_file.read().splitlines())


def get_final_message(win, tries, word):
    """Returns the final message of the game."""
    if win:
        return [
            'This... can\'t... be... happening...',
            'You win! You were incredibly lucky!',
            'By luck and skill, you win!',
            'Terrific!',
            'Nicely done!',
            'You win, but you can do better than that!',
            'You barely made it, yikes!',
            '?'
        ][tries]
    return f'You lost. The word was "{word}".'


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        prog='worder',
        description='Word guessing game.',
        epilog='Good luck!')
    parser.add_argument('-l', '--length', default="5")
    args = parser.parse_args()
    word_length = int(args.length)
    print(f"Guess a {word_length}-letter game in 6 tries.")
    while True:
        game = WorderGame(word_length)
        game.play()
        if input("One more (y/n)?").lower() != "y":
            break


if __name__ == '__main__':
    sys.exit(main())
