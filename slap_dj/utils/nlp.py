from typing import List


def is_english_word_alpha(word: str) -> bool:
    """Returns True when `word` is an English word. False otherwise.

    Args:
        word: Any given word

    Examples:
        >>> is_english_word_alpha("English")
        True
        >>> is_english_word_alpha("영원한")
        False
        >>> is_english_word_alpha("domestic")
        True
        >>> is_english_word_alpha("漢字")
        False
        >>> is_english_word_alpha("ひらがな")
        False
    """
    return word.upper() != word.lower()


def extract_eng_words(words: List[str]) -> List[str]:
    return list(filter(is_english_word_alpha, words))
