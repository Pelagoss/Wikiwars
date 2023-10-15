import requests
import urllib.parse
from bs4 import BeautifulSoup

def randomize_page():
    r = requests.get("https://fr.wikipedia.org/w/api.php?format=json&action=query&generator=random&grnnamespace=0")
    pages = r.json()['query']['pages']

    title = pages[list(dict(pages).keys())[0]]['title']
    title = str.replace(title, " ", "_")
    return title


def get_wiki_page(title):
    url = f'/wiki/{title}'

    # if 'w/index.php' in title and "#mw-pages" in title:
    #     url = title
    # https://fr.wikipedia.org/w/index.php?title=Cat%C3%A9gorie:Portail:Am%C3%A9rique_du_Sud/Articles_li%C3%A9s&pagefrom=Abarema+longipedunculata#mw-pages
    url = f'https://fr.wikipedia.org{url}'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, features="lxml")

    page_py = soup.find('div', class_='mw-content-container')
    [o.decompose() for o in page_py.find_all(class_='mw-editsection')]
    [o.decompose() for o in page_py.find_all(class_='vector-toc-landmark')]
    [o.decompose() for o in page_py.find_all(class_='vector-page-toolbar')]
    [o.decompose() for o in page_py.find_all(class_='mw-kartographer-maplink')]
    [o.decompose() for o in page_py.find_all(id='vector-toc-collapsed-button')]
    [o.decompose() for o in page_py.find_all(id='p-lang-btn')]
    [o.decompose() for o in page_py.find_all('span', id='coordinates')]
    [o.decompose() for o in page_py.find_all('sup', class_='reference')]

    for a in page_py.find_all('a', href=True):
        link_text = a['href']

        if a.find('img') is not None:
            a.replaceWithChildren()
            pass
        elif "/wiki/" in link_text and "/wiki/Aide:" not in link_text and "/wiki/Sp%C3%A9cial:" not in link_text and "/wiki/Discussion:" not in link_text and "/wiki/Mod%C3%A8le:" not in link_text and "https" not in link_text:
            pass
        elif '/w/index.php?title=' in link_text and "#mw-pages" in link_text:
            a['title'] = link_text.replace(
                f'/w/index.php?title={urllib.parse.quote(a["title"].replace(" ", "_"), safe=":/")}', f'{a["title"]}?')
            pass
        else:
            a.replaceWith(a.text)

    for a in page_py.find_all('a', href=False):
        a.replaceWith(a.text)

    for img in page_py.find_all('img'):
        if img["src"].startswith("//"):
            img["src"] = f'https:{img["src"]}'

    return page_py.prettify()


def getSummaryWikiPage(title):
    url = f'https://fr.wikipedia.org/api/rest_v1/page/summary/{title}?redirect=true'
    data = requests.get(url)

    return data.json()


def to_dict(o):
    if o is None:
        return o
    return o.to_dict()
