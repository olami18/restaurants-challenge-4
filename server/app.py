from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

from models import db, Restaurant,Pizza,RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
# create a response for landing page

class Home(Resource):
    def get(self):
        response_message = {
            "message": "WELCOME TO THE PIZZA RESTAURANT API."
        }
        return make_response(response_message, 200)


api.add_resource(Home, '/')
# deals with restaurant routes 
class Restaurants(Resource):
# get all restaurants 
    def get(self):
        restaurants = []
        for restaurant  in Restaurant.query.all():
            restaurant_dict={
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address
            }
            restaurants.append(restaurant_dict)
        return make_response(jsonify(restaurants), 200)

    

api.add_resource(Restaurants, '/restaurants')

# deals with restaurant routes
class RestaurantByID(Resource):
# get restaurants by id 
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            restaurant_dict={
                "id": restaurant.id,
                "name": restaurant.name,
                "address": restaurant.address,
                "pizzas":[
                    {
                        "id": restaurant_pizza.pizza.id,
                        "name": restaurant_pizza.pizza.name,
                        "ingredients": restaurant_pizza.pizza.ingredients
                    }
                    for restaurant_pizza in restaurant.pizzas
                ]
            }
            return make_response(jsonify(restaurant_dict), 200)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)

# delete a restaurant
    def delete(self,id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return make_response("", 204)
        else:
            return make_response(jsonify({"error": "Restaurant not found"}), 404)



api.add_resource(RestaurantByID, '/restaurants/<int:id>')
# deals with  pizzas routes
class Pizzas(Resource):

    def get(self):
        pizzas = []
        for pizza in Pizza.query.all():
            pizza_dict={
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            }
            pizzas.append(pizza_dict)
        return make_response(jsonify(pizzas), 200)
api.add_resource(Pizzas, '/pizzas')

# deals with api routes
class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()

        # Validate that the required fields are present in the request
        if not all(key in data for key in ("price", "pizza_id", "restaurant_id")):
            return make_response(jsonify({"errors": ["validation errors.include all keys"]}), 400)

        price = data["price"]
        pizza_id = data["pizza_id"]
        restaurant_id = data["restaurant_id"]

        # Check if the Pizza and Restaurant exist
        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)

        if not pizza or not restaurant:
            return make_response(jsonify({"errors": ["validation errors pizza and restaurant dont exist"]}), 400)

        # Create a new RestaurantPizza
        restaurant_pizza = RestaurantPizza(
            price = data["price"],
            pizza_id = data["pizza_id"],
            restaurant_id = data["restaurant_id"]

        )

        db.session.add(restaurant_pizza)
        db.session.commit()

        # Return data related to the Pizza
        pizza_data = {
            "id": pizza.id,
            "name": pizza.name,
            "ingredients": pizza.ingredients
        }

        return make_response(jsonify(pizza_data), 201)
api.add_resource(RestaurantPizzas,'/restaurant_pizzas')   
 # deals with not found errors
@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        "Not Found: The requested resource does not exist.",
        404
    )
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)