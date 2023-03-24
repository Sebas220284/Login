from flask import Flask,render_template,g,redirect,request,url_for,session,Response,jsonify
from functools import wraps
import database as dbase  
from product import Product

from pymongo import MongoClient
db = dbase.dbConnection()

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
   
   

MONGO_URI='mongodb+srv://sebastianvazquez:wGiHCSAq6xObqiEw@cluster0.fkwhctf.mongodb.net/?retryWrites=true&w=majority'



from users import routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    products = db['products']
    productsReceived = products.find()
    return render_template('dashboard.html', products = productsReceived)

#Method Post
@app.route('/products', methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        product = Product(name, price, quantity)
        products.insert_one(product.toDBCollection())
        response = jsonify({
            'name' : name,
            'price' : price,
            'quantity' : quantity
        })
        return redirect(url_for('dashboard'))
    else:
        return notFound()

#Method delete
@app.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one({'name' : product_name})
    return redirect(url_for('dashboard'))

#Method Put
@app.route('/edit/<string:product_name>', methods=['POST'])
def edit(product_name):
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        products.update_one({'name' : product_name}, {'$set' : {'name' : name, 'price' : price, 'quantity' : quantity}})
        response = jsonify({'message' : 'Producto ' + product_name + ' actualizado correctamente'})
        return redirect(url_for('dashboard'))
    else:
        return notFound()

@app.errorhandler(404)
def notFound(error=None):
    message ={
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response



if __name__ == '__main__':
    app.run(debug=True, port=4000)