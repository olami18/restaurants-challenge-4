from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
    serialize_rules = ('-restaurants.pizza', '-restaurant.pizzas')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    restaurants = db.relationship('RestaurantPizza', back_populates='pizza')
    
    # create resaurant_pizza object
class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    serialize_rules = ('restaurant', 'pizza')
   
    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
     # Define relationships to Restaurant and Pizza models
    restaurant = db.relationship('Restaurant', back_populates='pizzas')
    pizza = db.relationship('Pizza', back_populates='restaurants')

    # Define a back reference to the Restaurant model
    @validates("price")
    def validate_price(self, key, value):
        if not (1 <= value <= 30):
            raise ValueError("Price must be between 1 and 30")
        return value

# create restaurant tablee
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    serialize_rules = ('-pizzas.restaurant', '-restaurant.pizzas')
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String)
    
    # Define a back reference to the RestaurantPizza model
    pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')
   # ensure that the  name is less than 50 characters 
    @validates("name")
    def validate_name(self, key, name):
        if name and len(name) > 50:
            raise ValueError("Name must be less than 50 characters in length")
        return name