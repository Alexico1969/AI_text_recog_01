
from os import getenv, environ
from flask import Flask, render_template, session, request, redirect, url_for, g
from helper import simplify, count_most, categorize
from db import create_tables, add_initial_ai_data, get_ai_dict, add_knowledge, update_ai, repair_db


app=Flask(__name__, static_url_path='/static')

app.secret_key = 'Bruce Wayne is Batman'

create_tables()
add_initial_ai_data()

top_10 = []


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
    global top_10

    if request.method == "POST":
        print()
        print("-----------------------")
        print()
        input = request.form.get("text_input")
        input_words = input.split(" ")
        length = len(input_words)
        if length < 20:
            msg = f"{length} words is not enough to perform tasks on"
            return render_template("message.html", msg=msg)
        simplified = simplify(input)
        print("simplyfied: ", simplified)
        top_10 = count_most(simplified)
        wl = input.split(" ")
        inp_small = f"{wl[0]} {wl[1]} {wl[2]} ... {wl[-3]} {wl[-2]} {wl[-1]}"
        prediction = categorize(top_10, simplified).replace("_"," ")
        return render_template("result.html", input=inp_small, top_10=top_10, prediction=prediction)

    return render_template("examine.html")

@app.route('/result', methods=["POST"])
def result():
    global top_10
    category = request.form.get('input_cat')
    category = category.replace(" ","_")
    result = add_knowledge(category, top_10)
    msg = f"{result} {category}"
    return render_template("message.html", msg=msg)

@app.route('/train', methods=["GET","POST"])
def train():
    ai_dict = get_ai_dict()

    if request.method == "POST":
        action = request.form.get("word")
        print("action:", action)
        action_list = action.split(" ")
        category = action_list[0]
        word = action_list[1]
        temp_string = ai_dict[category]
        new_string = temp_string.replace(word + " ","")
        if temp_string == new_string:
            new_string = temp_string.replace(word,"")
            new_string = new_string[:-1]
            print(f"new_string: *{new_string}*")
        update_ai(category, new_string)
        ai_dict = get_ai_dict()

    
    new_dict = {}
    for el in ai_dict:
        temp_list = []
        words_splitted = ai_dict[el].split(" ")
        new_dict[el] = words_splitted

    return render_template("train.html", ai_dict=new_dict)

   

@app.route('/conversation')
def conversation():
    return render_template("conversation.html")

@app.route('/dump')
def dump():
    ai_dict = get_ai_dict()
    return render_template("dump.html", ai_dict=ai_dict)

@app.route('/repair')
def repair():
    result = repair_db()
    return render_template("message.html", msg=result)


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

