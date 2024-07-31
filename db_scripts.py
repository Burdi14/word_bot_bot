import psycopg2

INSERT_NEW_ADMIN = "INSERT INTO admins (user_id) VALUES {user_id};"

FIND_ADMIN = "SELECT exists (SELECT 1 FROM admins WHERE user_id = {user_id} LIMIT 1)"

conn = psycopg2.connect("dbname=word_bot user=burdi password=")

cur = conn.cursor()

def find_admin(user_id):
    cur.execute(FIND_ADMIN.format(user_id=user_id))
    res = cur.fetchone()
    return res