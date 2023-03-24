from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class Users:

  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  def signup(self):
    print(request.form)

    # Create the user object
    users = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "telefono": request.form.get('telefono'),
      "password": request.form.get('password')
    }

    # Encrypt the password
    users['password'] = pbkdf2_sha256.encrypt(users['password'])

    # Check for existing email address
    if db.user.find_one({ "email": users['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400

    if db.user.insert_one(users):
      return self.start_session(users)

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):

    users = db.user.find_one({
      "email": request.form.get('email')
    })

    if users and pbkdf2_sha256.verify(request.form.get('password'), users['password']):
      return self.start_session(users)
    
    return jsonify({ "error": "Invalid login credentials" }), 401