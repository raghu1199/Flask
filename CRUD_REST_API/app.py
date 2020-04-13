import pymysql
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:159159@localhost/flask_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

    def __repr__(self):
        return f"<Product {self.name}>"


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'qty')

    """
    id=ma.auto_field()
    name=ma.auto_field()
    description=ma.auto_field()
    price=ma.auto_field()
    qty=ma.auto_field()"""


product_schema1 = ProductSchema()
product_schema = ProductSchema(many=True)


@app.route("/product", methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name=name, description=description, price=price, qty=qty)
    db.session.add(new_product)
    db.session.commit()
    # result=product_schema1.dump(new_product)

    return product_schema1.jsonify(new_product)


# get all products
@app.route("/product", methods=['GET'])
def get_all_products():
    all_products = Product.query.all()
    result = product_schema.dump(all_products)
    print(result)
    return jsonify(result)


# get single product
@app.route("/product/<int:id1>", methods=['GET'])
def get_product(id1):
    product = Product.query.get_or_404(id1)
    print(product.name)
    return product_schema1.jsonify(product)


# update product
@app.route("/product/<id>", methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()
    return product_schema1.jsonify(product)


# delete
@app.route("/product/<id>", methods=['DELETE'])
def delete_prodcut(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema1.jsonify(product)


@app.route("/", methods=['GET'])
def index():
    return jsonify({'msg': 'HEllo world'})


if __name__ == "__main__":
    app.run(debug=True)
