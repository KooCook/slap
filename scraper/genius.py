import requests
from bs4 import BeautifulSoup


def main():
    page = requests.get('https://genius.com/Billie-eilish-bad-guy-lyrics')
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    return soup.find('a', **{'class':'lyrics'}).get_text()
