import zlib


def calculate_repetition(text: str, method: str = 'DEFLATE') -> float:
    b_str = bytes(text, encoding='utf-8')
    if method == 'DEFLATE':
        # default level = 6
        res = zlib.compress(b_str)
    else:
        raise NotImplementedError("Other methods not supported yet")
    ratio = len(res) / len(b_str)
    return 1 - ratio


if __name__ == '__main__':
    import re
    with open('tests/data/G.U.Y.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    cleaned_lines = [line for line in lines if re.match(f'^\[.*]\\n?$', line) is None]
    cleaned_text = ''.join(cleaned_lines)
    # print(cleaned_text)
    print(calculate_repetition(cleaned_text))
