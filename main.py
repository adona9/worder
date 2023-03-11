import random
import re
import sys


def get_random_word():
    """Grabs a random word from the given dictionary."""
    with open('./words', encoding='utf-8') as word_file:
        dictionary = word_file.read().splitlines()
    random.seed()
    chosen = int(round(random.random() * len(dictionary), 0))
    return dictionary[chosen]


def compare_guess(guess, word, used_letters):
    """Returns uppercase letters when the guessed letter is in the correct place
    and lowercase letters when the letter is in the mystery word, but it's in the wrong
    place."""
    outcome = ''
    for i in range(0, len(word)):
        if guess[i] == word[i]:
            outcome += guess[i].upper()
        elif guess[i] in word:
            outcome += guess[i].lower()
        else:
            outcome += '.'
            used_letters.add(guess[i])
    return outcome, used_letters


def is_word_valid(word):
    """Returns True if a word is in the dictionary."""
    if len(word) != 5:
        print(f'{word} is not a 5-letter word. Try again.')
        return False
    pattern = re.compile(f'{word}')
    with open('./words', encoding='utf-8') as word_file:
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
            if is_word_valid(guess):
                break
        guesses.append(guess)
        outcome, used_letters = compare_guess(guess, word, used_letters)
        outcomes.append(outcome)
        for guessed, result in zip(guesses, outcomes):
            print(f'        | {guessed} | {result} |')
        if outcome.lower() == word:
            return True
        for letter in sorted(alphabet - used_letters):
            print(f'{letter} ', end='')
        print('')
        guess_counter += 1
    return False


def main():
    """Main function."""
    word = get_random_word()
    if play_game(word):
        print('You win!')
    else:
        print(f'The word was "{word}"')


if __name__ == '__main__':
    sys.exit(main())
