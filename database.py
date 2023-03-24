from pymongo import MongoClient
import certifi

import pymongo



MONGO_URI='mongodb+srv://sebastianvazquez:wGiHCSAq6xObqiEw@cluster0.fkwhctf.mongodb.net/?retryWrites=true&w=majority'

ca = certifi.where()

def dbConnection():
    try:
        client = pymongo.MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["dbb_products_app"]
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db