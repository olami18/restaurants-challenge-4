from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_marshmallow import Marshmallow
db = SQLAlchemy()
ma = Marshmallow()
# RestaurantPizza many-to-many relationship table
restaurant_pizzas = db.Table('restaurant_pizzas',
                             db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.id'), primary_key=True),
                             db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id'), primary_key=True),
                             db.Column('price', db.Float, nullable=False)
                             )
# Restaurant Model
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(200))
    pizzas = db.relationship('Pizza', secondary=restaurant_pizzas, backref=db.backref('restaurants', lazy='dynamic'))
    @validates('name')
    def validate_name(self, key, name):
        assert len(name) <= 50, "Must have a name less than 50 words in length"
        return name
# Pizza Model
class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    ingredients = db.Column(db.String(200))
# Restaurant Schema
class RestaurantSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address')
# Pizza Schema
class PizzaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'ingredients')
restaurant_schema = RestaurantSchema()
restaurants_schema = RestaurantSchema(many=True)
pizza_schema = PizzaSchema()
pizzas_schema = PizzaSchema(many=True)