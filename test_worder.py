"""Unit tests for worder.py"""
import unittest
from unittest.mock import patch

from worder import WorderGame, blank_out_first_occurrence, get_final_message


class TestBlankOutFirstOccurrence(unittest.TestCase):
    def test_blanks_first_match_only(self):
        word = ['e', 'e', 'e']
        blank_out_first_occurrence(word, 'e')
        self.assertEqual(word, [' ', 'e', 'e'])

    def test_blanks_correct_position(self):
        word = ['a', 'b', 'a', 'c']
        blank_out_first_occurrence(word, 'a')
        self.assertEqual(word, [' ', 'b', 'a', 'c'])

    def test_no_match_leaves_word_unchanged(self):
        word = ['a', 'b', 'c']
        blank_out_first_occurrence(word, 'x')
        self.assertEqual(word, ['a', 'b', 'c'])


class TestGetFinalMessage(unittest.TestCase):
    def test_loss_includes_secret_word(self):
        self.assertIn('crane', get_final_message(False, 6, 'crane'))

    def test_win_returns_nonempty_string_for_all_valid_tries(self):
        for tries in range(1, 7):
            msg = get_final_message(True, tries, 'crane')
            self.assertIsInstance(msg, str)
            self.assertGreater(len(msg), 0)


class TestTileMarking(unittest.TestCase):
    """Tests for the guess-scoring logic embedded in WorderGame.play()."""

    def _score_guess(self, secret, guess):
        """Run one guess against a fixed secret and return the resulting tile row."""
        dictionary = {secret, guess}
        with patch('worder.load_dictionary', return_value=dictionary), \
             patch('random.choice', return_value=secret), \
             patch('builtins.input', side_effect=[guess, secret]), \
             patch('builtins.print'):
            game = WorderGame(len(secret))
            game.play()
        return game.tile_rows[0]

    def test_all_correct(self):
        tiles = self._score_guess('crane', 'crane')
        self.assertTrue(all(t.is_correct for t in tiles))

    def test_all_wrong(self):
        # 'foist' shares no letters with 'crane'
        tiles = self._score_guess('crane', 'foist')
        self.assertTrue(all(t.is_wrong for t in tiles))

    def test_partial_match(self):
        # secret: crane (c,r,a,n,e)  guess: ropes (r,o,p,e,s)
        # r → partial (in word, wrong position)
        # o, p, s → wrong
        # e → partial (in word, wrong position)
        tiles = self._score_guess('crane', 'ropes')
        self.assertTrue(tiles[0].is_partially_correct)   # r
        self.assertTrue(tiles[1].is_wrong)                # o
        self.assertTrue(tiles[2].is_wrong)                # p
        self.assertTrue(tiles[3].is_partially_correct)   # e
        self.assertTrue(tiles[4].is_wrong)                # s

    def test_correct_takes_priority_over_extra_occurrence(self):
        # secret: crane  guess: cacti
        # c at pos 0: correct
        # a at pos 1: partial (a is in crane but wrong position)
        # c at pos 2: wrong (the only 'c' in the secret was already matched)
        tiles = self._score_guess('crane', 'cacti')
        self.assertTrue(tiles[0].is_correct)              # c — correct position
        self.assertTrue(tiles[1].is_partially_correct)   # a — in word, wrong position
        self.assertTrue(tiles[2].is_wrong)                # c — no spare 'c' in secret

    def test_double_letter_in_guess_only_one_marked_partial(self):
        # secret: crane (one 'e' at pos 4)  guess: every (e,v,e,r,y)
        # Neither 'e' in the guess is at the correct position (pos 4).
        # Only the first 'e' should be marked partial; the second 'e' should be wrong.
        tiles = self._score_guess('crane', 'every')
        self.assertTrue(tiles[0].is_partially_correct)   # first 'e' — partial
        self.assertTrue(tiles[1].is_wrong)                # v
        self.assertTrue(tiles[2].is_wrong)                # second 'e' — wrong, quota used up
        self.assertTrue(tiles[3].is_partially_correct)   # r — partial
        self.assertTrue(tiles[4].is_wrong)                # y


if __name__ == '__main__':
    unittest.main()
