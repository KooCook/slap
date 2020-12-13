import zlib
from typing import List, Iterator, Dict, Iterable
from operator import itemgetter

import pandas as pd
from scipy.optimize import curve_fit

from app.utils.misc import depreciated


def calculate_repetition(text: str, method: str = 'DEFLATE') -> float:
    b_str = bytes(text, encoding='utf-8')
    if method == 'DEFLATE':
        # default level = 6
        res = zlib.compress(b_str)
    else:
        raise NotImplementedError("Other methods not supported yet")
    ratio = len(res) / len(b_str)
    return 1 - ratio


def get_words(s: str) -> Iterator[str]:
    it = iter(s)
    lst = []
    for c in it:
        if c in ' -,\n()"':
            yield ''.join(lst)
            lst = []
        else:
            lst.append(c)


def get_sorted_bag_of_words(words: Iterable[str]) -> Dict[str, str]:
    bow = {}
    for word in words:
        word = word.lower()
        bow[word] = bow.get(word, 0) + 1
    sorted_bow = dict(sorted(bow.items(), key=itemgetter(1), reverse=True))
    return sorted_bow


@depreciated(reason="Use get_bow_dataframe() for better perf")
def convert_bow_to_dataframe(sorted_bow: Dict[str, str]) -> pd.DataFrame:
    lst = []
    for r, (k, v) in enumerate(sorted_bow.items()):
        lst.append({
            'freq': v,
            'rank': r + 1,
            'word': k,
        })
    df = pd.DataFrame(lst)
    return df


def get_bow_dataframe(words: Iterable[str]) -> pd.DataFrame:
    bow = {}
    for word in words:
        word = word.lower()
        bow[word] = bow.get(word, 0) + 1
    sorted_bow = sorted(bow.items(), key=itemgetter(1), reverse=True)
    lst = []
    for r, (k, v) in zip(range(1, len(bow) + 1), sorted_bow):
        lst.append({
            'freq': v,
            'rank': r,
            'word': k,
        })
    df = pd.DataFrame(lst)
    return df


def zipf_getter(N: int):
    def zipf(k, s):
        # TODO: optimize using a stdlib function
        return (1 / k ** s) / sum(1 / n ** s for n in range(1, N + 1)) * N
    return zipf


def fit_to_zipf(df: pd.DataFrame) -> (float, float):
    """

    Args:
        df: A bag of words in a DataFrame format.

    Returns:
        s: Fitted value of the parameter (?) s of the zipf function.
        pcov: Covariant of the fitting (?) curve_fit.pcov
    """
    N = sum(df.get('freq'))
    zipf = zipf_getter(N)
    popt, pcov = curve_fit(zipf, df.get('rank'), df.get('freq'))
    return popt[0], pcov


def plot_line_fit_to_zipf(df: pd.DataFrame, s: float) -> None:
    N = sum(df.get('freq'))
    zipf = zipf_getter(N)
    plt.plot(df.get('rank'), df.get('freq'), 'b-', label='data')
    plt.plot(df.get('rank'), zipf(df.get('rank'), s), 'r-',
             label='fit: s=%5.3f' % s)
    # plt.plot(df.get('rank'), zipf(df.get('rank'), 1.07), 'g--',
    #          label='ctrl: s=1.07')
    plt.legend()
    plt.show()
    return


def plot_bar_comp_to_zipf(df: pd.DataFrame, s: float) -> None:
    N = sum(df.get('freq'))
    zipf = zipf_getter(N)
    L = 10
    plt.bar(df.get('word')[:L], df.get('freq')[:L])
    plt.bar(df.get('word')[:L], zipf(df.get('rank')[:L], s))
    plt.show()


if __name__ == '__main__':
    import re
    with open('tests/data/G.U.Y.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    cleaned_lines = [line for line in lines if re.match(f'^\[.*]\\n?$', line) is None]
    cleaned_text = ''.join(cleaned_lines)
    # print(cleaned_text)
    print(calculate_repetition(cleaned_text))
