"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# empiezan codigos para USER
# get para USER funciona en postman
@app.route('/user', methods=['GET'])
def get_user():

    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }
    user = User.query.all()
    all_users = list(map(lambda x: x.serialize(), User.query))
    return jsonify(all_users), 200

# GET para USER id funciona en postman url/user/numero-elegido
@app.route('/user/<int:id>', methods=['GET'])
def get_userid(id):
    userid = User.query.get(id)
    result = userid.serialize()
    return jsonify(result), 200

# POST para USER funciona en postman
@app.route('/user', methods=['POST'])
def create_user():

    request_body_user = request.get_json()
    newuser = User(name=request_body_user["name"], email=request_body_user["email"], password=request_body_user["password"],is_active=request_body_user["is_active"])
    db.session.add(newuser)
    db.session.commit()
    return jsonify(request_body_user), 200

# empiezan codigos para people
# GET para PEOPLE funciona en postman
@app.route('/people', methods=['GET'])
def get_people():

    # response_body = {
    #     "msg": "Este es el GET para people "
    # }
    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), People.query))
    return jsonify(all_people), 200

# GEt ID para PEOPLE funciona en postman
@app.route('/people/<int:id>', methods=['GET'])
def get_peopleid(id):
    peopleid = People.query.get(id)
    result = peopleid.serialize()
    return jsonify(result), 200

# empiezan codigos para planet
@app.route('/planet', methods=['GET'])
def get_planet():

    # response_body = {
    #     "msg": "Este es el GET para planets"
    # }

    # return jsonify(response_body), 200

    planet = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), Planet.query))
    return jsonify(all_planets), 200

# GEt ID para PLANET funciona en postman
@app.route('/planet/<int:id>', methods=['GET'])
def get_planetid(id):
    planetid = Planet.query.get(id)
    result = planetid.serialize()
    return jsonify(result), 200

# empiezan codigos para Favoritos
# GET para FAVORITE según user, funciona en postman
@app.route('/user/<int:id>/favorite', methods=['GET'])
def get_fav(id):
    query = User.query.get(id)
    if query is None:
        return("El favorito no existe")
    else:
        result = Favorite.query.filter_by(user_id= query.id)
        fav_list = list(map(lambda f: f.serialize(), result))
        return jsonify(fav_list), 200

# POST para FAVORITE de c/USER
@app.route('/user/<int:id>/favorite', methods=['POST'])
def create_fav(id):

    solicitud = request.get_json()
    newfav = Favorite(user=id, favorite_character=solicitud["favorite_character"], favorite_planet=solicitud["favorite_planet"])
    db.session.add(newfav)
    db.session.commit()
    return jsonify("Favorito agregado")

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)