#Imports
import firebase_admin
import json
from firebase_admin import credentials, auth, db
from flask import Flask, request, render_template
#App configuration
#Connect to firebase
cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app(cred, {"databaseURL":"https://dealgetter-70e69-default-rtdb.firebaseio.com/"})
#pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))


ref = db.reference("/")

ref.set({
	"Users":-1
})

ref = db.reference("/Users")
ref.push().set(
    {
    "": {
        "Name":"as", 
        "Email":"asd",
        "Password":"asdf", 
        "Products": -1
        }
    }
)
ref.push().set(
    {
    "d": {
        "Name":"as", 
        "Email":"asdfd",
        "Password":"asdfghs", 
        "Products": -1
        }
    }
)
    

users = ref.get()
# print()
# print(users.keys())
# print (users.values())
for key in users.keys():
    print (key)
    for k in users[key].keys():
        print (users[key][k])
        if users[key][k]["Email"] == "asdfd":
            if users[key][k]["Password"] == "asdfghs":
                print ("good")
    
# ref.child("deetsadi").update({
#     "Products":tempDict
# })
