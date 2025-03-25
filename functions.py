import sqlite3

def getConnection():
    con = sqlite3.connect('test.db')
    return con

def define():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(username, mail, password)")
    #cursor.execute("CREATE TABLE IF NOT EXISTS stock(name, password)")
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

def cleanDb():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE users")
    connection.commit()
    connection.close()