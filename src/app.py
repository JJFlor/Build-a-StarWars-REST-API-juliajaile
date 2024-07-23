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
from models import db, User, Favourites, Characters, Planets, Vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
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

#USER CLASS ROUTES
@app.route('/get_users', methods=['GET'])
def get_users():
   users = User.query.all()
   users = [user.serialize() for user in users]
   if not users:
        return(jsonify({"msg":"No se encontraron los usuarios"})), 404
   
   response_body = {
        "user": users
    }
   return jsonify(response_body), 200

@app.route('/get_user/<int:id>', methods=['GET'])
def get_user(id):
   user = User.query.get(id)
   if not user:
        return(jsonify({"msg":"No se encontró el usuario"})), 404
   
   response_body = {
        "user": user
    }
   return jsonify(response_body), 200

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json #lo que manda el usuario en formato json
    if not data['email'] or not data['password']:
        return jsonify({'msg':'todos los campos son necesarios'}), 400
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'msg':'el usuario ya existe'}), 200
    new_user = User(email = data['email'], password = data['password'], is_active = True)
    db.sessions.add(new_user)
    db.sessions.commit()
    return jsonify({'msg':'OK', 'user': new_user.serialize()}), 201

@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'msg':'No se encontró el usuario a eliminar'}), 404
    db.sessions.delete(user)
    db.sessions.commit()
    return jsonify({'msg':'Usuario eliminado'})

@app.route('/edit_user/<int:id>', methods=['PUT'])
def edit_user(id):
    data = request.json
    if data['email'] and data['is_active']:
        user = User.query.get(id)
        if not user:
            return jsonify({'msg':'Error, no se encontró el usuario'}), 404
        user.email = data['email'] or user.email
        user.is_active = data['is_active'] or user.is_active
        db.sessions.commit()
        return jsonify({'msg':'Usuario editado', 'user': user.serialize()})


@app.route('/get_user_favourites/<int:id>', methods=['GET'])
def get_user_favourites(user_id):
   user_favourites = Favourites.query.get(user_id)
   if not user_favourites:
        return(jsonify({"msg":"No se encontró el favorito"})), 404
   
   response_body = {
        "user_favourites": user_favourites
    }
   return jsonify(response_body), 200

@app.route('/add_favourite_character/<int:id>', methods=['POST'])
def add_favourite_character(characters_id):
    data = Characters
    favourite_character = Favourites.query.get(characters_id)
    if not favourite_character:
        return jsonify({'msg':'selecciona un personaje favorito'}), 400
    favourite_character = Favourites.query.filter_by(characters_id).first()
    if favourite_character:
        return jsonify({'msg':'el personaje ya está en favoritos'}), 200
    new_favourite_character = Characters(name = data['name'], gender = data['gender'], hair_color = data['hair_color'], eye_color = data['eye_color'])
    db.sessions.add(new_favourite_character)
    db.sessions.commit()
    return jsonify({'msg':'OK', 'favourite_character': new_favourite_character.serialize()}), 201

@app.route('/add_favourite_planet/<int:id>', methods=['POST'])
def add_favourite_planet(planets_id):
    data = Planets
    favourite_planet = Favourites.query.get(planets_id)
    if not favourite_planet:
        return jsonify({'msg':'selecciona un planeta favorito'}), 400
    favourite_planet = Favourites.query.filter_by(planets_id).first()
    if favourite_planet:
        return jsonify({'msg':'el planeta ya está en favoritos'}), 200
    new_favourite_planet = Planets(name = data['name'], climate = data['climate'], gravity = data['gravity'], population = data['population'])
    db.sessions.add(new_favourite_planet)
    db.sessions.commit()
    return jsonify({'msg':'OK', 'favourite_planet': new_favourite_planet.serialize()}), 201

@app.route('/add_favourite_vehicle/<int:id>', methods=['POST'])
def add_favourite_vehicle(vehicles_id):
    data = Vehicles
    favourite_vehicle = Favourites.query.get(vehicles_id)
    if not favourite_vehicle:
        return jsonify({'msg':'selecciona un vehículo favorito'}), 400
    favourite_vehicle = Favourites.query.filter_by(vehicles_id).first()
    if favourite_vehicle:
        return jsonify({'msg':'el vehículo ya está en favoritos'}), 200
    new_favourite_vehicle = Vehicles(name = data['name'], model = data['model'], passengers = data['passengers'], speed = data['speed'])
    db.sessions.add(new_favourite_vehicle)
    db.sessions.commit()
    return jsonify({'msg':'OK', 'favourite_vehicle': new_favourite_vehicle.serialize()}), 201

@app.route('/delete_character/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = Characters.query.get(id)
    if not character:
        return jsonify({'msg':'No se encontró el personaje a eliminar'}), 404
    db.sessions.delete(character)
    db.sessions.commit()
    return jsonify({'msg':'Personaje eliminado'})

@app.route('/delete_planet/<int:id>', methods=['DELETE'])
def delete_planet(id):
    planet = Planets.query.get(id)
    if not planet:
        return jsonify({'msg':'No se encontró el planeta a eliminar'}), 404
    db.sessions.delete(planet)
    db.sessions.commit()
    return jsonify({'msg':'Planeta eliminado'})

@app.route('/delete_vehicle/<int:id>', methods=['DELETE'])
def delete_vehicle(id):
    vehicle = Vehicles.query.get(id)
    if not vehicle:
        return jsonify({'msg':'No se encontró el vehículo a eliminar'}), 404
    db.sessions.delete(vehicle)
    db.sessions.commit()
    return jsonify({'msg':'Vehículo eliminado'})


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
