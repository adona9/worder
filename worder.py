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


def get_random_word(word_length):
    """Grabs a random word from the given dictionary."""
    with open(f'./word{word_length}', encoding='utf-8') as word_file:
        dictionary = word_file.read().splitlines()
    random.seed()
    chosen = int(round(random.random() * len(dictionary), 0))
    return dictionary[chosen]


def compare_guess(guess, word, used_letters):
    """Returns uppercase letters when the guessed letter is in the correct place
    and lowercase letters when the letter is in the mystery word, but it's in the wrong
    place."""
    outcome = ''
    word_length = len(word)
    correct_counter = 0
    for index, letter in enumerate(word):
        if guess[index] == letter:
            correct_counter += 1
            outcome += f'{UiColors.OKGREEN}{letter.upper()}{UiColors.ENDC}'
        elif guess[index] in word:
            outcome += f'{UiColors.WARNING}{guess[index].lower()}{UiColors.ENDC}'
        else:
            outcome += '.'
            used_letters.add(guess[index])
    return outcome, used_letters, correct_counter == word_length


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


def play_game(word):
    """Plays a word guessing game."""
    alphabet = set('abcdefghijklmnopqrstuvwxyz')
    used_letters = set([])
    guess_counter = 1
    outcomes = []
    guesses = []
    while guess_counter < 7:
        while True:
            guess = input(f'Guess #{guess_counter}? ').lower()
            if is_word_valid(guess, len(word)):
                break
        guesses.append(guess)
        outcome, used_letters, won = compare_guess(guess, word, used_letters)
        outcomes.append(outcome)
        for guessed, result in zip(guesses, outcomes):
            print(f'        | {guessed.upper()} | {result} |')
        if won:
            return True, guess_counter
        for letter in sorted(alphabet - used_letters):
            print(f'{letter.upper()} ', end='')
        print('')
        guess_counter += 1
    return False, guess_counter


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
    word_length = args.length
    print(f"Guess a {word_length}-letter game in 6 tries.")
    while True:
        word = get_random_word(word_length)
        win, tries = play_game(word)
        print(get_final_message(win, tries, word))
        if input("One more (y/n)?").lower() != "y":
            break


if __name__ == '__main__':
    sys.exit(main())
