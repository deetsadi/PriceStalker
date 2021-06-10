#Imports
import firebase_admin
import pyrebase
import json
from firebase_admin import credentials, auth
from flask import Flask, request, render_template
#App configuration
app = Flask(__name__)
#Connect to firebase
cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))
#Data source
users = [{'uid': 1, 'name': 'Noah Schairer'}]


"""
@app.route('/login_data', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
        else:
            return render_template('index.html', products=products, deleted_products=deleted_products)
"""


#Api route to get users
@app.route('/')
def userinfo():
    return render_template("login.html")

#Api route to sign up a new user
@app.route('/login_data', methods=['GET', 'POST'])
def signup():
    email = request.form.get('username')
    password = request.form.get('password')

    if email is None or password is None:
        return {'message': 'Error missing email or password'},400
    try:
        user = auth.create_user(
               email=email,
               password=password
        )
        print ("we out")
        print ("User creation successful")
        return {'message': 'Successfully created user'+user.email},200
    except:
        return {'message': 'Error creating user'},400

#Api route to get a new token for a valid user
@app.route('/api/token')
def token():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except:
        return {'message': 'There was an error logging in'},400
if __name__ == '__main__':
    app.run(debug=True)