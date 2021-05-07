import requests
from bs4 import BeautifulSoup

from utils.cleaning import clean_string

URL_80 = 'https://www.gutenberg.org/files/103/103-h/103-h.htm'


def scrape_url(url: str):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all(['p'])
    text = [result.text for result in results]
    article = ' '.join(text)
    article = clean_string(article)
    return article

'''book = scrape_url(URL_80)
print(book)'''