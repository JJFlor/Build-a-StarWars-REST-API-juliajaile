from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email #self.X tiene que ser uno de ,los identificadores del User que me permita diferenciarlo de los demás 

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "user_name": self.user_name,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }

class Favourites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('users', lazy=True))

    characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    characters = db.relationship('Characters', backref=db.backref('characters', lazy=True))

    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planets = db.relationship('Planets', backref=db.backref('planets', lazy=True))

    vehicles_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    vehicles = db.relationship('Vehicles', backref=db.backref('vehicles', lazy=True))


    def __repr__(self):
        return '<Favourites %r>' % self.id 

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "characters_id": self.characters_id,
            "planets_id": self.planets_id,
            "vehicles_id": self.vehicles_id
        }
    

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(50), unique=True, nullable=False)
    hair_color = db.Column(db.String(50), unique=True, nullable=False)
    eye_color = db.Column(db.String(50), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Characters %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color
        }
   

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    climate = db.Column(db.String(50), unique=True, nullable=False)
    gravity = db.Column(db.Integer,unique=True, nullable=False)
    population = db.Column(db.Integer,unique=True, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.id 

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "gravity": self.gravity,
            "population": self.population
        }
    
    

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    model = db.Column(db.String(50), unique=True, nullable=False)
    passengers = db.Column(db.Integer,unique=True, nullable=False)
    speed = db.Column(db.Integer,unique=True, nullable=False)

    def __repr__(self):
        return '<Vehicles %r>' % self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "passengers": self.passengers,
            "speed": self.speed
          
        }