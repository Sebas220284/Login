from flask import Flask,jsonify,request,session,redirect
from passlib.hash import pbkdf2_sha256
from app import db
import uuid

class Users:

    def start_session(self,user):
       del user ['password']
       session['logged_in']=True
       session ['user']=user,200
      
      
       return jsonify(user)
    def signup(self):
    
       print(request.form)   
       users={

"_id": uuid.uuid4().hex,
"name": request.form.get('name'),
"email":request.form.get('email'),
"password":request.form.get('password')

    } 
       

       users['password']= pbkdf2_sha256.encrypt(users['password'])

       if db.user.find_one({"email": users['email']}):
           return jsonify({"error": "Este correo pertenece a otro usuario"}),400

       if db.user.insert_one(users):
        
        
        return self.start_session(users)
       
  
       return jsonify({"error":"registro fallido"}),400
 
    def signout(self):
   
       session.clear()
   
       return redirect('/')