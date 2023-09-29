from random import randint, choice as rc,sample
from faker import Faker
from app import app
from models import db, Pizza, RestaurantPizza, Restaurant
import random
fake = Faker()


pizza_names = [
    "Margherita Pizza",
    "Pepperoni Pizza",
    "Hawaiian Pizza",
    "BBQ Chicken Pizza",
    "Veggie Supreme Pizza",
    "Meat Lovers Pizza",
    "Mushroom and Olive Pizza",
    "Buffalo Chicken Pizza",
    "Four Cheese Pizza",
    "Pesto and Tomato Pizza",
    # You can add more pizza names here
]
pizza_ingredients = [
    "Dough",
    "Tomato sauce",
    "Mozzarella cheese",
    "Pepperoni",
    "Bell peppers",
    "Onions",
    "Mushrooms",
    "Olives",
    "Basil",
    "Oregano",
]


with app.app_context():
    db.session.query(RestaurantPizza).delete()
    db.session.query(Pizza).delete()
    db.session.query(Restaurant).delete()
    
    db.session.commit()
      
    # Create and add fake restaurants
    restaurants = [
        Restaurant( 
            name = fake.company() ,

            address=fake.address()
        )
        for i in range(10)
    ]
    db.session.add_all(restaurants)  # Use db.session.add_all() to add the list
    db.session.commit()

    # Create and add fake pizzas
    pizzas = [
        Pizza(
            name=pizza_name,
            ingredients=', '.join(sample(pizza_ingredients, 3)) 
        )
        for pizza_name in pizza_names
    ]
    db.session.add_all(pizzas)  # Use db.session.add_all() to add the list
    db.session.commit()

    # Create restaurant-pizza relationships
    restaurant_pizzas = [
        RestaurantPizza(
            pizza_id=random.choice(pizzas).id,
            restaurant_id=random.choice(restaurants).id,
            price=random.randint(1, 30)
        )
        for i in range(10)
    ]
    db.session.add_all(restaurant_pizzas)  # Use db.session.add_all() to add the list
    db.session.commit()
