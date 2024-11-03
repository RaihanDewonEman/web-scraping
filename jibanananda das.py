import requests
from bs4 import BeautifulSoup
import csv


def detail_page(_page_links, _headers):
    for _page in _page_links:
        try:
            _url = _page['href']
            _response = requests.get(_url, headers=_headers)
            _soup = BeautifulSoup(_response.content, features="html.parser")
            title = _soup.find('div', class_='entry-header').find("h1").get_text()
            book = _soup.find('table', class_='customdata-table').find_all("td")[-1].get_text()
            poem = _soup.find('div', class_='entry-the-content').find("p")
        except Exception as e:
            print(e, title)
            continue
        yield {'title': title, 'book': book, 'poem': poem}


url = "https://www.poetrystate.com/p/jibanananda/"
# Some servers may return a 406 error if the User-Agent header is missing or doesn’t match common browser signatures.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, features="html.parser")
page_links = soup.find('table').find_all("a")

file_name = 'poem.csv'
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Book", "Poem"])
    for poem in detail_page(page_links, headers):
        writer.writerow([poem['title'], poem['book'], poem['poem']])

