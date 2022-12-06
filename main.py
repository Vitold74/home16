import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import data

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }

class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }

def init_database():
    db.drop_all()
    db.create_all()

    for user_data in data.user:
        new_user = User(
            id=user_data['id'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            age=user_data['age'],
            email=user_data['email'],
            role=user_data['role'],
            phone=user_data['phone']
        )

        db.session.add(new_user)
        db.session.commit()

    for order_data in data.orders:
        new_order = Order(
            id=order_data['id'],
            name=order_data['name'],
            description=order_data['description'],
            start_date=order_data['start_date'],
            end_date=order_data['end_date'],
            address=order_data['address'],
            price=order_data['price'],
            customer_id=order_data['customer_id'],
            executor_id=order_data['executor_id']
        )
        db.session.add(new_order)
        db.session.commit()

    for offer_data in data.offers:
        new_offer = Offer(
            id=offer_data['id'],
            order_id=offer_data['order_id'],
            executor_id=offer_data['executor_id'],
        )
        db.session.add(new_offer)
        db.session.commit()


@app.route ("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        result = []
        for u in User.query.all():
            result.append(u.to_dict())

            return json.dumps(result), 200

    if request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            id=user_data['id'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            age=user_data['age'],
            email=user_data['email'],
            role=user_data['role'],
            phone=user_data['phone']
        )

        db.session.add(new_user)
        db.session.commit()

        return "User created", 201

@app.route ("/user/<int:uid>", methods=["GET", "PUT", "DELETE"])
def user(uid):
    if request.method == "GET":
        return json.dumps(User.query.get(uid).to_dict()), 200

    if request.method == "PUT":
        user_data = json.loads(request.data)
        u = User.query.get(uid)
        u.first_name = user_data["first_name"]
        u.last_name = user_data["last_name"]
        u.age = user_data["age"]
        u.email = user_data["email"]
        u.role = user_data["role"]
        u.phone = user_data["phone"]

        db.session.add(u)
        db.session.commit()

        return "User updated", 204

    if request.method == "DELETE":
        u = User.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "User deleted", 204

@app.route ("/orders", methods=["GET", "POST"])
def orders():
    if request.method == "GET":
        result = []
        for u in Order.query.all():
            result.append(u.to_dict())

            return json.dumps(result), 200

    if request.method == "POST":
        order_data = json.loads(request.data)
        new_order = Order(
            id=order_data['id'],
            name=order_data['name'],
            description=order_data['description'],
            start_date=order_data['start_date'],
            end_date=order_data['end_date'],
            address=order_data['address'],
            price=order_data['price'],
            customer_id=order_data['customer_id'],
            executor_id=order_data['executor_id']
        )
        db.session.add(new_order)
        db.session.commit()

        return "Order created", 201

@app.route ("/order/<int:uid>", methods=["GET", "PUT", "DELETE"])
def order(uid):
    if request.method == "GET":
        return json.dumps(Order.query.get(uid).to_dict()), 200

    if request.method == "PUT":
        order_data = json.loads(request.data)
        u = Order.query.get(uid)
        u.name = order_data["name"]
        u.description = order_data["description"]
        u.start_date = order_data["start_date"]
        u.end_date = order_data["end_date"]
        u.address = order_data["address"]
        u.price = order_data["price"]
        u.customer_id = order_data["customer_id"]
        u.executor_id = order_data["executor_id"]

        db.session.add(u)
        db.session.commit()

        return "Order updated", 204

    if request.method == "DELETE":
        u = Order.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "Order deleted", 204

@app.route("/offers", methods=["GET", "POST"])
def offers():
    if request.method == "GET":
        result = []
        for u in Offer.query.all():
            result.append(u.to_dict())

            return json.dumps(result), 200

    if request.method == "POST":
        offer_data = json.loads(request.data)
        new_offer = Offer(
            id=offer_data['id'],
            order_id=offer_data['order_id'],
            executor_id=offer_data['executor_id'],
        )
        db.session.add(new_offer)
        db.session.commit()
        return "Offer created", 201

@app.route ("/offer/<int:uid>", methods=["GET", "PUT", "DELETE"])
def offer(uid):
    if request.method == "GET":
        return json.dumps(Offer.query.get(uid).to_dict()), 200

    if request.method == "PUT":
        offer_data = json.loads(request.data)
        u = Offer.query.get(uid)
        u.order_id = offer_data["order_id"]
        u.executor_id = offer_data["executor_id"]

        db.session.add(u)
        db.session.commit()

        return "Offer updated", 204

    if request.method == "DELETE":
        u = Offer.query.get(uid)

        db.session.delete(u)
        db.session.commit()

        return "Offer deleted", 204

if __name__ == '__main__':
    init_database()
    app.run()







