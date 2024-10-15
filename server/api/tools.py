import requests
import urllib.parse
from .models import Game, User, Email, Friendship, Avatar
from .application import db
from bs4 import BeautifulSoup
from flask import render_template
from flask_mail import Mail
from flask_mail import Message
from threading import Thread
import uuid

from flask import current_app

mailer = Mail()

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
            a['href'] = link_text.replace(
                f'/w/index.php?title={urllib.parse.quote(a["title"].replace(" ", "_"), safe=":/")}', f'/wiki/{a["title"]}?')
            pass
        else:
            a.replaceWith(a.text)

    for a in page_py.find_all('a', href=False):
        a['onclick'] = 'return false'
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

def send_async_email(app, msg):
    with app.app_context():
        mailer.send(msg)

def send_mail(type_mail, user, data, sync=False):
    if isinstance(user, str):
        recipients = [user]
    else:
        recipients = [user.email]

    appUrl = current_app.config['APP_URL']
    appUrlBack = current_app.config['APP_URL_BACK']

    data['appUrl'] = appUrl
    data['appUrlBack'] = appUrlBack

    for key, value in data.items():
        data[key] = value.replace('[appUrl]', appUrl)

    if type_mail == 'register':
        subject = 'Confirmez votre inscription !'
    elif type_mail == 'registerRelance':
        subject = '[Relance] Confirmez votre inscription !'
    else:
        subject = 'Consultez les WikiNews !'

    msg = Message(
        subject=subject,
        sender=(current_app.config['MAIL_SENDER'], current_app.config['MAIL_ADDRESS']),
        recipients=recipients
    )

    unique_token = uuid.uuid4()

    data['browserLink'] = f'{appUrl}/emails/{unique_token}'

    msg.html = render_template(
            "mail/{}.html".format(type_mail),
            **data
        )

    emails = Email.from_message(msg)
    for email in emails:
        email.unique_token = unique_token
        email.type = type_mail
        email.recipient_id = user.id

        db.session.add(email)
        db.session.flush()
        db.session.commit()

    if sync:
        mailer.send(msg)
    else:
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()

    return None
