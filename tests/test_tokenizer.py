import unittest

from services import genius
from dirs import ROOT_DIR


class TokenizerTest(unittest.TestCase):
    tokenizer = genius.tokenize_words

    def test_tokenizer(self):
        self.maxDiff = None
        test_cases = [
            ('lyrics/bad-romance.txt',
             'lyrics/bad-romance-words.txt'),
            ('lyrics/cheap-thrills.txt',
             'lyrics/cheap-thrills-words.txt'),
            ('lyrics/G.U.Y.txt',
             'lyrics/G.U.Y-words.txt'),
        ]
        for input_file, expected_result_file in test_cases:
            with self.subTest(f"{input_file=} {expected_result_file=}"):
                with open(ROOT_DIR / 'tests/data' / input_file, 'r', encoding='utf-8') as file:
                    input_ = file.read()
                with open(ROOT_DIR / 'tests/data' / expected_result_file, 'r', encoding='utf-8') as file:
                    expected_result = file.read().splitlines(keepends=False)
                self.assertEqual(expected_result, self.__class__.tokenizer(input_))


if __name__ == '__main__':
    unittest.main()
