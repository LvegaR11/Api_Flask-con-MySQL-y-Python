from flask import Flask
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
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    
    db.create_all()

class  UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'created_at', 'updated_at')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/users', methods=['POST'])
def create_user():

    print(request.json)
    return 'Usuario recivido'