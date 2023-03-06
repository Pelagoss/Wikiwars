import requests
from bs4 import BeautifulSoup


def randomize_page():
    r = requests.get("https://fr.wikipedia.org/w/api.php?format=json&action=query&generator=random&grnnamespace=0")
    pages = r.json()['query']['pages']

    title = pages[list(dict(pages).keys())[0]]['title']
    title = str.replace(title, " ", "_")
    return title

def get_wiki_page(title):
    url = f'https://fr.wikipedia.org/api/rest_v1/page/html/{title}?redirect=true'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, features="lxml")

    page_py = soup.find('body')
    [o.decompose() for o in page_py.find_all('sup', class_='reference')]

    for a in page_py.find_all('a', href=True, rel=True):
        link_text = a['href']
        rel = a['rel']

        if "mw:WikiLink" in rel and 'class' not in a.attrs.keys():
            pass
        elif a.find('img') is not None and "./" in link_text:
            pass
        else:
            a.replaceWith(a.text)

    for img in page_py.find_all('img'):
        if img["src"].startswith("//"):
            img["src"] = f'https:{img["src"]}'

    return page_py.prettify()


def to_dict(o):
    if o is None:
        return o
    return o.to_dict()