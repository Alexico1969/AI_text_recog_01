import sqlite3, os
from flask import g
import psycopg2
from urllib import parse

#sqlite = sqlite3.connect('approot/ai.db', check_same_thread=False)
sqlite = sqlite3.connect('ai.db', check_same_thread=False)
sql = sqlite.cursor()

def create_tables():
    sql.execute('''create table if not exists topics
        (topic_id integer primary key autoincrement,
        name text,
        word_list text)
    ''')
    sql.execute('''create table if not exists irrelevant_words
        (topic_id integer primary key autoincrement,
        word text)
    ''')
    sql.execute('''create table if not exists punctuation
        (topic_id integer primary key autoincrement,
        symbol text)
    ''')    

    print("tables are created")
    
def add_topic(name, word_list):
    sql.execute('''insert into topics(name, word_list) values(?,?)''', 
    [name, word_list])
    sqlite.commit()
    return True

def add_initial_ai_data():
    add_topic("miscellanious", "general xylophone enigma")
    add_topic("geopolitics", "russia china putin anthony blinken vladimir putin africa asia europe xi jinping")
    add_topic("infrastructure", "car road roads interstate turnpike railroad airport wheel driver")
    add_topic("social media", "facebook fwitter instagram tweet post youtube whatsapp account reply comment")
    add_topic("celebrities", "famous oscar movie actor actress hollywood singer album ep song interview")
    return True

def get_ai_dict():
    result = sql.execute("select * from topics")
    data = result.fetchall()
    output = {}
    for item in data:
        output[item[1]] = item[2]
    return output    
    
def add_knowledge(category, top_10):
    current_knowledge = get_ai_dict()
    temp_str = ""
    if category in current_knowledge:
        temp_str = current_knowledge[category]
        output = "Key words were added to category "
    else:
        output = "The following category was added: "
    for word in top_10:
            temp_str += " " + word
    add_topic(category, temp_str)
    return output
        