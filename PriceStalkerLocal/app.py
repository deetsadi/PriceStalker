import firebase_admin
import unicodedata
import json
import random
from firebase_admin import credentials, auth, db
from flask import Flask, render_template, request, redirect, url_for, session
from scraper import get_product_details, extract_url


app = Flask(__name__)
app.secret_key = "super secret key"
app.config["SESSION_TYPE"] = "filesystem"

products = []
deleted_products = []

cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app(cred, {"databaseURL":"https://dealgetter-70e69-default-rtdb.firebaseio.com/"})
ref = db.reference("/Users")
current_user = ""
current_user_uid = ""

@app.route('/')
def main():
    return render_template('signup.html')

@app.route('/login_data', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = (unicodedata.normalize('NFKD', request.form.get('email')).encode('ascii', 'ignore')).decode('UTF-8')
        password = (unicodedata.normalize('NFKD', request.form.get('password')).encode('ascii', 'ignore')).decode('UTF-8')
        if email is None or password is None:
            return {'message': 'Error missing email or password'},400
        users = ref.get()
        for key in users.keys():
            for k in users[key].keys():
                #print (users[key][k])
                if users[key][k]["Email"] == email:
                    if users[key][k]["Password"] == password:
                        session["key"] = key+"/"+k
                        print (session["key"])
                        p1 = (ref.child(session["key"]).get())["Products"]
                        if checkDeletedExists(ref.child(session["key"]).get()):
                            d1 = (ref.child(session["key"]).get())["Deleted"]
                        else:
                            d1 = []
                        return render_template('index.html', products=p1[1:], deleted_products=d1)
        products = []
        deleted_products = []
        return render_template("login.html", error="Error. Incorrect username or password.")

def getUser():  
    return current_user      

@app.route('/signup_data', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        name = (unicodedata.normalize('NFKD', request.form.get('name')).encode('ascii', 'ignore')).decode('UTF-8')
        email = (unicodedata.normalize('NFKD', request.form.get('email')).encode('ascii', 'ignore')).decode('UTF-8')
        password = (unicodedata.normalize('NFKD', request.form.get('password')).encode('ascii', 'ignore')).decode('UTF-8')
        if email is None or password is None:
            return {'message': 'Error missing email or password'},400
        ref.push().set(
            {
            name: {
                "Name":name, 
                "Email":email,
                "Password":password, 
                "Products": ["test"],
                "Deleted" : ["test"]
                }
            }
        )
        users = ref.get()
        print (users)
        for key in users.keys():
            for k in users[key].keys():
                #print (users[key][k])
                if users[key][k]["Email"] == email:
                    if users[key][k]["Password"] == password:
                        session["key"] = key+"/"+k
        return render_template("index.html", products=[], deleted_products=[])

@app.route('/switch_to_login', methods=['POST', 'GET'])
def switch_to_login():
    if request.method == 'POST':
        if request.form['switch'] == 'Login Instead':
            return render_template('login.html')


@app.route('/switch_to_signup', methods=['POST', 'GET'])
def switch_to_signup():
    if request.method == 'POST':
        if request.form['switch'] == 'Sign Up Instead':
            return render_template('signup.html')


@app.route('/add_item', methods=["POST"])
def got_url():
    url = request.form['task']

    key = session["key"]
    user = ref.child(key).get()
    p1 = user["Products"]

    if checkDeletedExists(ref.child(session["key"]).get()):
        d1 = (ref.child(session["key"]).get())["Deleted"]
    else:
        d1 = []

    details = get_product_details(url)

    for i in user["Products"][1:]:
        if i["url"] == details["url"]:
            return render_template('index.html', products=p1[1:], deleted_products=d1)

    details = get_product_details(url)

    if details != None:
        p1.append(get_product_details(url))

        ref.child(key).update({
            "Products":p1
        })

    return render_template('index.html', products=p1[1:], deleted_products=d1)


@app.route('/delete', methods=['GET', 'POST'])
def delete():

    p1 = (ref.child(session["key"]).get())["Products"]

    if checkDeletedExists(ref.child(session["key"]).get()):
        d1 = (ref.child(session["key"]).get())["Deleted"]
    else:
        d1 = []

    index = 0
    for i in range(len(p1)):
        if i == 0:
            continue
        if p1[i]["url"] == request.form['delete']:
            index = i

    d1.append(p1[index])
    p1.remove(p1[index])

    key = session["key"]

    ref.child(key).update({
        "Products":p1,
        "Deleted":d1
    })

    return render_template('index.html', products=p1[1:], deleted_products=d1)

@app.route('/delete_deleted_products', methods=['GET', 'POST'])
def delete_deleted_products():
    index = 0
    p1 = (ref.child(session["key"]).get())["Products"]
    
    if checkDeletedExists(ref.child(session["key"]).get()):
        d1 = (ref.child(session["key"]).get())["Deleted"]
    else:
        d1 = []

    for i in range(len(d1)):
        if d1[i]["url"] == request.form['delete_deleted_products']:
            index = i
    del (d1[index])

    key = session["key"]
    ref.child(key).update({
        "Deleted":d1
    })

    return render_template('index.html', products=p1[1:], deleted_products=d1)


def checkDeletedExists(user):
    if "Deleted" in user.keys():
        return True
    return False