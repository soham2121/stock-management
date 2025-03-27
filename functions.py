import sqlite3
import re, random

def getConnection():
    con = sqlite3.connect('test.db')
    return con

def define():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(username, mail, password)")
    cursor.execute("CREATE TABLE IF NOT EXISTS stock(id AUTO_INCREMENT, user, name, category, price, quantity, expiry)")
    cursor.execute("CREATE TABLE IF NOT EXISTS session(username, password)")
    connection.commit()
    connection.close()

def checkUser(username):
    con = getConnection()
    c = con.cursor()
    c.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username=? LIMIT 1)", (username,))
    record = c.fetchone()
    if(record[0] == 1):
        return True
    else:
        return False

def checkMail(mail):
    con = getConnection()
    c = con.cursor()
    c.execute("SELECT EXISTS(SELECT 1 FROM users WHERE mail=? LIMIT 1)", (mail,))
    record = c.fetchone()
    if(record[0] == 1):
        return True
    else:
        return False
    
def checkPassword(user):
    con = getConnection()
    c = con.cursor()
    c.execute("SELECT password FROM users where username=?", (user,))
    record = c.fetchone()
    return record[0]

def checkPassValid(password):
    if(len(password) < 8):
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif ' ' in password:
        return False
    else:
        return True

def cleanDb():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE users")
    cursor.execute("DROP TABLE session")
    cursor.execute("DROP TABLE stock")
    connection.commit()
    connection.close()

def getItems(user):
    con = getConnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM stock where user=?", (user,))
    record = cur.fetchall()
    con.commit()
    con.close()
    return record

def makeId():
    con = getConnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM stock")
    record = cur.fetchall()
    id = random.randint(100000, 999999)
    for records in record:
        if(records[0] == id):
            id = random.randint(100000, 999999)
    return id

def getItem(id):
    con = getConnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM stock where id=?", (id,))
    record = cur.fetchone()
    con.commit()
    con.close()
    return record

# cleanDb()
# define()