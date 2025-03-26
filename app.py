from flask import Flask, render_template, request, redirect
from functions import getConnection, define, checkUser, checkMail, checkPassword

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

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
        elif(password != confirm):
            return render_template("signup.html", error = "Both passwords are not the same")
        elif(password == "" or username == "" or confirm == ""):
            return render_template("signup.html", error = "All fields are required")
        elif(password == confirm):
            connection = getConnection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, mail, password) VALUES (?, ?, ?)", (username, mail, password))
            connection.commit()
            connection.close()
            return redirect('/List')

    return render_template("signup.html")

@app.route("/Login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = str(request.form['name'])
        password = str(request.form['password'])
        check = checkPassword(username)

        if(checkUser(username) == 0):
            return render_template("login.html", error = "User is invalid")
        elif(password == check):
            return redirect('/List')
        else:
            return render_template("login.html", error = "Password is incorrect")
    return render_template("login.html")

@app.route("/List")
def List():
    return render_template("stockList.html")

define()

if __name__ == "__main__":
    app.run(debug=True)