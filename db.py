import sqlite3, os
from flask import g
#import psycopg2
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

    sql.execute('''create table if not exists statistics
        (stat_id integer primary key autoincrement,
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
    add_topic("social_media", "facebook fwitter instagram tweet post youtube whatsapp account reply comment")
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
        temp_str += word + " "
    l = len(temp_str)
    temp_str = temp_str[:l-1]
    print("temp_str: ", temp_str)
    add_topic(category, temp_str)
    return output
        
def update_ai(category, new_string):
    sql.execute("update topics set word_list=? where name=?", (new_string, category) )
    sqlite.commit()

def repair_db():
    ai_dict = get_ai_dict()
    for cat in ai_dict:
        temp_str = ai_dict[cat]
        temp_str.replace("  "," ")
        update_ai(cat, temp_str)
    return "The database has been repaired"

def clear_db():
    sql.execute('''drop table topics''')
    create_tables()
    add_initial_ai_data()
    return "Table 'topics' is reset."

def execute_query(query):
    sql.execute(query)
    sqlite.commit()
    return f"Query '{query}' was executed"

def check_empty_categories():
    counter = 0
    ai_dict = get_ai_dict()
    for cat in ai_dict:
        temp_str = ai_dict[cat]
        if len(temp_str) < 3:
            sql.execute('''delete from topics where name=?''',  [cat] )
            sqlite.commit()
            counter += 1
    msg = f"{counter} empty categories were removed"
    print(msg)
    return