from flask import Flask, render_template
from flaskwebgui import FlaskUI   # get the FlaskUI class
import wikipedia


app = Flask(__name__)
ui = FlaskUI(app)                 # feed the parameters


# do your logic as usual in Flask

@app.route("/")
def index():
    wikipedia.set_lang("fr")
    page_py = wikipedia.page("Germany").html()
    return render_template("main.twig.html", page=page_py)

@app.route("/wiki/<title>")
def next(title):
    print(title)
    wikipedia.set_lang("fr")
    page_py = wikipedia.page(title, auto_suggest=False).html()
    return render_template("main.twig.html", page=page_py)

ui.run()                           # call the 'run' method 