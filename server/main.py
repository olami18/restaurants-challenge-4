from flask import Flask, request, jsonify
from models import db, ma, Restaurant, Pizza, restaurant_pizzas, restaurant_schema, restaurants_schema, pizza_schema, pizzas_schema
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma.init_app(app)
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    all_pizzas = Pizza.query.all()
    return jsonify(pizzas_schema.dump(all_pizzas))
@app.route("/restaurant_pizzas", methods=["POST"])
def post_restaurant_pizzas():
    try:
        new_restaurant_pizza = restaurant_pizzas.insert().values(
            price=request.json['price'], pizza_id=request.json['pizza_id'], restaurant_id=request.json['restaurant_id'])
        db.session.execute(new_restaurant_pizza)
        db.session.commit()
        pizza = Pizza.query.get(request.json['pizza_id'])
        return pizza_schema.jsonify(pizza), 201
    except Exception:
        return jsonify({"errors": ["validation errors"]}), 422