import json
import argparse

def xprint(i: int, msg: str):
    print('  ' * i, end='')
    print(msg)


def yaml(key: str, value: object, i: int = 0):
    xprint(i, f'{key}:')
    yaml_value(value, i)


def yaml_value(value: object, i: int = 0):
    if isinstance(value, int):
        xprint(i, '  type: integer')
    elif isinstance(value, str):
        xprint(i, '  type: string')
    elif isinstance(value, float):
        xprint(i, '  type: number')
    elif isinstance(value, bool):
        xprint(i, '  type: boolean')
    elif isinstance(value, list):
        xprint(i, '  type: array')
        xprint(i, '  items:')
        if value:
            yaml_value(value[0], i+1)
        else:
            xprint(i, '  NULLL')
    elif isinstance(value, dict):
        xprint(i, '  type: object')
        xprint(i, '  properties:')
        for k, v in value.items():
            yaml(k, v, i + 2)


def main():
    parser = argparse.ArgumentParser(description='Autogenerate OpenAPI schema from JSON')
    parser.add_argument('filename', type=str,
                        help='JSON file name to parse')
    args = parser.parse_args()
    with open(args.filename, 'r', encoding='utf-8') as f:
        res: dict = json.load(f)

    for k, v in res.items():
        yaml(k, v)


if __name__ == '__main__':
    main()
