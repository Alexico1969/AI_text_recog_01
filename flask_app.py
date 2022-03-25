
from os import getenv, environ
from flask import Flask, render_template, session, request, redirect, url_for, g
from helper import simplify, count_most, count_most_weighed, categorize


app=Flask(__name__, static_url_path='/static')

app.secret_key = 'Bruce Wayne is Batman'

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
   return "login"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   return "signup"

@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect(url_for('home_page'))

@app.route('/examine', methods=["GET","POST"])
def examine():
    if request.method == "POST":
        input = request.form.get("text_input")
        simplified = simplify(input)
        top_10 = count_most(simplified)
        inp_small = input[:3] + " ... " + input[-3:]
        render_template("result.html", input=inp_small, top_10=top_10)

    return render_template("examine.html")

@app.route('/train')
def train():

    return render_template("train.html")

@app.route('/conversation')
def conversation():

    return render_template("conversation.html")



# Do not alter this if statement below
# This should stay towards the bottom of this file
if __name__ == "__main__":
    flask_env = getenv('FLASK_ENV')
    if flask_env != 'production':
        environ['FLASK_ENV'] = 'development'
        app.debug = True
        app.asset_debug = True
        server = Server(app.wsgi_app)
        server.serve()
    app.run()

