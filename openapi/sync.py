import yaml

if __name__ == '__main__':
    with open("slap-api.yaml") as f:
        dct = yaml.load(f)
    with open("slap-api-server.yaml") as f:
        dct2 = yaml.load(f)
        dct2['paths'] = dct['paths']
    yaml.dump(dct2, open('slap-api-server.yaml', 'w'))
