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
                        return render_template('index.html', products=[], deleted_products=[])
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
                "Products": ["test"]
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
        products = []
        deleted_products = []
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
    details = get_product_details(url)
    print(getUser())
    if details != None:
        products.append(get_product_details(url))
        key = session["key"]

        user = ref.child(key).get()
        print (user)
        dict1 = user["Products"]
        dict1.append(url)

        ref.child(key).update({
            "Products":dict1
        })
    return render_template('index.html', products=products, deleted_products=deleted_products)


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    index = 0
    for i in range(len(products)):
        if products[i]["url"] == request.form['delete']:
            index = i
    deleted_products.append(products[index])
    del products[index]
    print (deleted_products)
    return render_template('index.html', products=products, deleted_products=deleted_products)

@app.route('/delete_deleted_products', methods=['GET', 'POST'])
def delete_deleted_products():
    index = 0
    for i in range(len(deleted_products)):
        if deleted_products[i]["url"] == request.form['delete_deleted_products']:
            index = i
    del deleted_products[index]
    return render_template('index.html', products=products, deleted_products=deleted_products)