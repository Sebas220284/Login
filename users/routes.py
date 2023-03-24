from flask import Flask
from app import app
from users.models import Users

@app.route('/users/signup', methods=['POST'])
def signup():
  return Users().signup()

@app.route('/users/signout')
def signout():
  return Users().signout()

@app.route('/users/login', methods=['POST'])
def login():
  return Users().login()

 