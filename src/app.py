from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from  flask_marshmallow import Marshmallow

#Ceamos una variavle global que guarda el objeto de la clase Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/api_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #isntanciamos la clase SQLAlchemy
ma = Marshmallow(app) #Instanciamos la clase Marshmallow

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    last_name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), nullable=False)
   
    def __init__(self, id, name, last_name, email, password):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password


# Crear el esquema de la clase User
class  UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'last_name', 'email', 'password')

user_schema = UserSchema()# Esquema para un solo usuaro
users_schema = UserSchema(many=True) # Esquema para un listado de usuarios

# ENDPOINT para crear un usuario
@app.route('/users', methods=['POST'])
def create_user():

    id = request.json['id']
    name = request.json['name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']

    new_user = User(id, name, last_name, email, password) #Creamos el objeto User
    db.session.add(new_user)##Agregamos el nuevo objeto a la base de datos
    db.session.commit()##Guardamos los cambios en la base de datos

    return user_schema.jsonify(new_user)##Retornamos el objeto User en formato JSON


# ENDPOINT para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all() #Obtenemos todos los objetos User de la base de datos
    result = users_schema.dump(all_users) #Retornamos el objeto User en formato JSON
    return jsonify(result)


# ENDPOINT para obtener un usuario
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id) #Obtenemos el objeto User de la base de datos
    return user_schema.jsonify(user) #Retornamos el objeto User en formato JSON


# ENDPOINT para actualizar un usuario
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id) #Obtenemos el id User de la base de datos que queremos actualizar
    # Obtenemos los datos del request
    name = request.json['name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']

    # Actualizamos los datos del objeto User
    user.name = name
    user.last_name = last_name
    user.email = email
    user.password = password
    db.session.commit()

    return user_schema.jsonify(user)


# ENDPOINT para eliminar un usuario
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return '¡Usuario eliminado Exitosamente'


if __name__ == '__main__':
    # Crear la tablas de la base de datos
    with app.app_context():
        db.create_all()
    app.run(debug=True)     #Ejecutamos la aplicacion