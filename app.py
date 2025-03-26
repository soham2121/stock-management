from flask import Flask, render_template, request, redirect, url_for
from functions import getConnection, define, checkUser, checkMail, checkPassword, checkPassValid, getItems

app = Flask(__name__)
currentUser = None

@app.route("/")
def basic():
    return redirect('/Home')

@app.route("/Home")
def home():
    return render_template("home.html")

@app.route("/SignOut")
def signout():
    global currentUser
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM session")
    record = cursor.fetchall()
    username = record[0][0]
    cursor.execute("DELETE FROM session WHERE username=?", (username,))
    connection.commit()
    connection.close()
    currentUser = None
    return redirect('/Home')

@app.route("/Signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = str(request.form['name'])
        mail = str(request.form['mail'])
        password = str(request.form['password'])
        confirm = str(request.form['confirmPassword'])
        
        if(checkMail(mail)):
            return render_template("signup.html", error = "An account is already created with this mail")
        elif(checkUser(username)):
            return render_template("signup.html", error = "Username already taken")
        elif(checkPassValid(password) == False):
            return render_template("signup.html", passerror = True)
        elif(password != confirm):
            return render_template("signup.html", error = "Both passwords are not the same")
        elif(password == "" or username == "" or confirm == ""):
            return render_template("signup.html", error = "All fields are required")
        elif(password == confirm):
            connection = getConnection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, mail, password) VALUES (?, ?, ?)", (username, mail, password))
            cursor.execute("INSERT INTO session (username, password) VALUES (?, ?)", (username, password))
            connection.commit()
            connection.close()
            return redirect('/List')

    return render_template("signup.html")

@app.route("/Login", methods = ['GET', 'POST'])
def login():
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM session")
    record = cursor.fetchall()
    if(len(record) > 1):
        cursor.execute("DROP TABLE session")
        connection.commit()
        connection.close()
    elif(record == []):
        if request.method == 'POST':
            username = str(request.form['name'])
            password = str(request.form['password'])
            check = checkPassword(username)

            if(checkUser(username) == 0):
                return render_template("login.html", error = "User is invalid")
            elif(password == "" or username == ""):
                return render_template("login.html", error = "All fields are required")
            elif(password == check):
                cursor.execute("INSERT INTO session (username, password) VALUES (?, ?)", (username, password))
                connection.commit()
                connection.close()
                return redirect('/List')
            else:
                return render_template("login.html", error = "Password is incorrect")
    else:
        connection.commit()
        connection.close()
        return redirect('/List')
    return render_template("login.html")

@app.route("/List", methods = ['GET', 'POST'])
def list():
    global currentUser
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM session")
    record = cursor.fetchall()
    currentUser = record[0][0]
    items = getItems(currentUser)
    connection.commit()
    connection.close()
    return render_template("stockList.html", username = currentUser, items = items)

@app.route("/AddStock", methods = ['GET', 'POST'])
def addStock():
    if request.method == 'POST':
        global currentUser
        name = str(request.form['name'])
        category = str(request.form['category'])
        price = str(request.form['price'])
        quantity = str(request.form['quantity'])
        expiry = str(request.form['expiry'])
        if(expiry == ''):
            expiry = "~"

        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO stock VALUES (?, ?, ?, ?, ?, ?)", (currentUser, name, category, price, quantity, expiry))
        connection.commit()
        connection.close()

        return redirect('/List')
    
    return render_template("addStock.html")
        
define()

if __name__ == "__main__":
    app.run(debug=True)