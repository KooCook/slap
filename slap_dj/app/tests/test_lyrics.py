import unittest

from app.services import genius
from dirs import ROOT_DIR

TEST_DATA_DIR = ROOT_DIR / 'testdata'


class LyricsTest(unittest.TestCase):
    tokenizer = genius.tokenize_words
    LYRICS_TEST_DATA_DIR = TEST_DATA_DIR / 'lyrics'

    def test_tokenizer(self):
        self.maxDiff = None
        test_cases = [
            ('bad-romance.txt',
             'bad-romance-words.txt'),
            ('cheap-thrills.txt',
             'cheap-thrills-words.txt'),
            ('G.U.Y.txt',
             'G.U.Y-words.txt'),
            ('animals.txt',
             'animals-words.txt'),
        ]
        for input_file, expected_result_file in test_cases:
            with self.subTest(f"{input_file=} {expected_result_file=}"):
                with open(self.LYRICS_TEST_DATA_DIR / input_file, 'r', encoding='utf-8') as file:
                    input_ = file.read()
                with open(self.LYRICS_TEST_DATA_DIR / 'expected' / expected_result_file, 'r', encoding='utf-8') as file:
                    expected = file.read().splitlines(keepends=False)
                actual = self.__class__.tokenizer(input_)
                with open(self.LYRICS_TEST_DATA_DIR / 'actual' / expected_result_file, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(actual) + '\n')
                self.assertEqual(expected, actual)

    remove_sections = genius.remove_sections

    def test_remove_sections(self):
        self.maxDiff = None
        test_cases = [
            ('bad-romance.txt',
             'bad-romance-no-sections.txt'),
            ('animals.txt',
             'animals-no-sections.txt'),
        ]
        for input_file, expected_result_file in test_cases:
            with self.subTest(f"{input_file=} {expected_result_file=}"):
                with open(self.LYRICS_TEST_DATA_DIR / input_file, 'r', encoding='utf-8') as file:
                    input_ = file.read()
                with open(self.LYRICS_TEST_DATA_DIR / 'expected' / expected_result_file, 'r', encoding='utf-8') as file:
                    expected = file.read()
                actual = self.__class__.remove_sections(input_)
                with open(self.LYRICS_TEST_DATA_DIR / 'actual' / expected_result_file, 'w', encoding='utf-8') as file:
                    file.write(actual)
                self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
