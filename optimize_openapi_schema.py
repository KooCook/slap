from yaml import load
from pprint import pprint


class Pattern:
    instances = []

    def __init__(self, filename: str, name: str = None):
        if name is None:
            self.name: str = filename.split('.')[0]
        else:
            self.name = name
        with open(filename, 'r', encoding='utf-8') as f:
            dct = load(f)
        self.dict: dict = dct
        self.instances.append(self)


def match(value: object):
    if isinstance(value, dict):
        for pattern in Pattern.instances:
            if value == pattern.dict:
                return pattern.name
            for k, v in value.items():
                if k not in pattern.dict:
                    break
                if v != pattern.dict.get(k):
                    break
            else:
                return pattern.name
    return None


def yaml(dct: dict):
    for k, v in dct.items():
        if isinstance(v, dict):
            if v.get('type') == 'object':
                pattern = match(v['properties'])
                if pattern is not None:
                    dct[k] = {'$ref': f'#/components/schemas/{pattern}'}
                    continue
            yaml(v)


def main():
    files = [
        ('Artist.yaml', 'Artist'),
        ('Artist-2.yaml', 'Artist'),
    ]
    for file, name in files:
        Pattern(file, name)

    with open('song-response.yaml', 'r', encoding='utf-8') as f:
        dct = load(f)
    yaml(dct)
    pprint(dct)


if __name__ == '__main__':
    main()
