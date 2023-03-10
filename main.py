import random
import re
import sys


def get_random_word():
    with open('./words') as f:
        dictionary = f.read().splitlines()
    random.seed()
    chosen = int(round(random.random() * len(dictionary), 0))
    return dictionary[chosen]


def compare_guess(guess, word, used_letters):
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


def is_word_valid(w):
    if len(w) != 5:
        print(f'{w} is not a 5-letter word. Try again.')
        return False
    pattern = re.compile(f'{w}')
    with open('./words') as f:
        dictionary = f.read()
    is_in_dictionary = pattern.search(dictionary)
    if not is_in_dictionary:
        print(f'{w} is not in the dictionary. Try again.')
        return False
    return True


def play_game(word):
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
        for g, o in zip(guesses, outcomes):
            print(f'        | {g} | {o} |')
        if outcome.lower() == word:
            return True
        for letter in sorted(alphabet - used_letters):
            print(f'{letter} ', end='')
        print('')
        guess_counter += 1
    return False


def main():
    word = get_random_word()
    if play_game(word):
        print('You win!')
    else:
        print(f'The word was "{word}"')


if __name__ == '__main__':
    sys.exit(main())