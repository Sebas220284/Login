from flask import Flask,render_template,g,redirect,request,url_for,session
from functools import wraps


from pymongo import MongoClient

app =Flask (__name__)
app.secret_key="\xc2\xf6\xee\x1cD\xf4p'\x03B;\xf7\x87\xa8\xcf\xdf"

def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap
  
    
         
client= MongoClient('mongodb://localhost:27017/user')
db=client.user
   
   


from users import routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    
 return render_template('dashboard.html')
