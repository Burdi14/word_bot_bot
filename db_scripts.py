import psycopg2
import psycopg2.extras
INSERT_NEW_USER = "INSERT INTO users (user_id, username) VALUES ({user_id}, '{username}');"
GET_USERS = "SELECT user_id FROM users;"
DELETE_USER = "DELETE FROM users WHERE user_id = {user_id};"

FIND_ID_BY_USERNAME = "SELECT user_id FROM users WHERE username = '{username}' LIMIT 1;"

INSERT_NEW_ADMIN = "INSERT INTO admins  VALUES ({user_id});"
DELETE_ADMIN = "DELETE FROM admins WHERE user_id = {user_id};"
FIND_ADMIN = "SELECT exists (SELECT 1 FROM admins WHERE user_id = {user_id} LIMIT 1);"

INSERT_WORD= "INSERT INTO words (word, definition, description, is_sent) VALUES ('{word}', '{definition}', '{description}','{is_sent}');"
GET_UNUSED_WORDS = "SELECT word FROM words WHERE is_sent = false;"
FIND_WORD = "SELECT (word, definition, description) FROM words WHERE word = '{word}';"
UPDATE_WORD = "UPDATE words SET definition = '{definition}', description ='{description}', is_sent = '{is_sent}' WHERE word = '{word}';"
DELETE_WORD = "DELETE FROM words WHERE word = '{word}';"

conn = psycopg2.connect("dbname=word_bot user=burdi password=")

cur = conn.cursor()

def delete_word(word):
    cur.execute(DELETE_WORD.format(word=word))
    conn.commit()
def update_word(word, definition, description, is_sent):
    cur.execute(UPDATE_WORD.format(word=word,  definition=definition, description=description, is_sent=is_sent))
    conn.commit()
def insert_word(word, definition, description, is_sent):
    cur.execute(INSERT_WORD.format(word=word, definition=definition, description=description, is_sent=is_sent))
    conn.commit()

def delete_admin(user_id):
    cur.execute(DELETE_ADMIN.format(user_id=user_id))
    conn.commit()

def find_id_by_username(username):
    cur.execute(FIND_ID_BY_USERNAME.format(username=username))
    id = cur.fetchone()
    return id
def insert_new_addmin(user_id):
    cur.execute(INSERT_NEW_ADMIN.format(user_id=user_id))
    conn.commit()
def find_word(word):
    cur.execute(FIND_WORD.format(word=word))
    res = cur.fetchall()
    for row in res:
        print(row)

    return word

def insert_new_user(user_id, username):
    cur.execute(INSERT_NEW_USER.format(user_id=user_id, username=username))
    conn.commit()
    
def find_admin(user_id):
    cur.execute(FIND_ADMIN.format(user_id=user_id))
    res = cur.fetchone()
    return res[0]
    

def get_unused_words():
    cur.execute(GET_UNUSED_WORDS)
    res = cur.fetchall()
    return res

def get_active_users():
    cur.execute(GET_USERS)
    return cur.fetchall()