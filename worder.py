#!/usr/bin/python3
"""Main program of a word guessing game."""
import argparse
import random
import re
import sys


# pylint: disable-next=R0903
class UiColors:
    """Definitions of UI colors"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class WorderGame:
    """Represents a round in the game of Worder"""

    def __init__(self, word_length):
        self.word_length = word_length
        self.alphabet = set('abcdefghijklmnopqrstuvwxyz')
        self.used_letters = set([])
        self.outcomes = []
        self.guesses = []
        self.won = False

    def play(self):
        word = get_random_word(self.word_length)
        guess_counter = 1
        while guess_counter < 7:
            guess = self.read_guess(guess_counter)
            self.guesses.append(guess)
            outcome = ''
            correct_counter = 0
            for index, letter in enumerate(word):
                if guess[index] == letter:
                    correct_counter += 1
                    outcome += f'{UiColors.OKGREEN}{letter.upper()}{UiColors.ENDC}'
                elif guess[index] in word:
                    outcome += f'{UiColors.WARNING}{guess[index].lower()}{UiColors.ENDC}'
                else:
                    outcome += '.'
                    self.used_letters.add(guess[index])
            self.won = correct_counter == self.word_length
            self.outcomes.append(outcome)
            for guessed, result in zip(self.guesses, self.outcomes):
                print(f'        | {guessed.upper()} | {result} |')
            if self.won:
                break
            for letter in sorted(self.alphabet - self.used_letters):
                print(f'{letter.upper()} ', end='')
            print('')
            guess_counter += 1
        print(get_final_message(self.won, guess_counter, word))

    def read_guess(self, guess_counter):
        """Read a guess from stdin"""
        while True:
            guess = input(f'Guess #{guess_counter}? ').lower()
            if is_word_valid(guess, self.word_length):
                break
        return guess


def get_random_word(word_length):
    """Grabs a random word from the given dictionary."""
    with open(f'./word{word_length}', encoding='utf-8') as word_file:
        dictionary = word_file.read().splitlines()
    random.seed()
    chosen = int(round(random.random() * len(dictionary), 0))
    return dictionary[chosen]


def is_word_valid(word, word_length):
    """Returns True if a word is in the dictionary."""
    if len(word) != word_length:
        print(f'{word} is not a {word_length}-letter word. Try again.')
        return False
    pattern = re.compile(f'{word}')
    with open(f'./word{word_length}', encoding='utf-8') as word_file:
        dictionary = word_file.read()
    is_in_dictionary = pattern.search(dictionary)
    if not is_in_dictionary:
        print(f'{word} is not in the dictionary. Try again.')
        return False
    return True


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
