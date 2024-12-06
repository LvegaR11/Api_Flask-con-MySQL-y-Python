from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from  flask_marshmallow import Marshmallow

#Ceamos una variavle global que guarda el objeto de la clase Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/api_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, name, last_name, email, password):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password
    

# Crear el esquema de la clase User
class  UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'last_name', 'email', 'password', 'created_at', 'updated_at')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# ENDPOINT para crear un usuario
@app.route('/users', methods=['POST'])
def create_user():

    print(request.json)
    return 'Recivido'

if __name__ == '__main__':
    with app.app_context(): #Creamos un contexto de la aplicacion
        db.create_all()     #Creamos la tabla de la base de datos
    app.run(debug=True)     #Ejecutamos la aplicacion