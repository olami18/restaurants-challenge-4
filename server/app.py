from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import validates
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
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
        assert len(name) <= 50
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
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    all_restaurants = Restaurant.query.all()
    return restaurants_schema.jsonify(all_restaurants)
@app.route("/restaurants/<id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return jsonify({"error": "Restaurant not found"})
    else:
        result = restaurant_schema.dump(restaurant).data
        result['pizzas'] = [pizza_schema.dump(pizza).data for pizza in restaurant.pizzas]
        return jsonify(result)
@app.route("/restaurants/<id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant is None:
        return jsonify({"error": "Restaurant not found"})
    else:
        db.session.delete(restaurant)
        db.session.commit()
        return restaurant_schema.jsonify(restaurant)
if __name__ == '__main__':
    app.run()