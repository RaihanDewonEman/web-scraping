import requests
from bs4 import BeautifulSoup
import csv


def detail_page(_page_links, _headers):
    if _page_links is None:
        return []

    for _page in _page_links:
        _title = ""
        try:
            _url = _page['href']
            _response = requests.get(_url, headers=_headers)
            _soup = BeautifulSoup(_response.content, features="html.parser")

            _title = _soup.find("div", class_="entry-header").find("h1").get_text()
            _poem_paras = _soup.find("div", class_="entry-the-content").find_all("p")
            _poem = ""
            for poem_para in _poem_paras:
                for poem_br_tag in poem_para.find_all("br"):
                    poem_br_tag.replace_with("")

            for poem_para in _poem_paras:
                _poem += poem_para.get_text()
        except Exception as e:
            print(e)
            continue
        yield {"title": _title, "poem": _poem}


url = "https://www.poetrystate.com/p/jibanananda/"
# Some servers may return a 406 error if the User-Agent header is missing or doesn’t match common browser signatures.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
}

file_name = "poem.csv"
with open(file_name, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Poem"])

while True:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, features="html.parser")

    page_links = soup.find("table").find_all("a") if soup.find("table") else None

    with open(file_name, mode="a", newline="") as file:
        writer = csv.writer(file)
        for poem in detail_page(page_links, headers):
            writer.writerow([poem["title"], poem["poem"]])

    next_page = soup.find(class_="nav-links").find("a", class_="next page-numbers")
    if next_page:
        url = next_page['href']
    else:
        break
