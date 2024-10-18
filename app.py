from flask import Flask, render_template, jsonify, request, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from models import db, Product, Category, User


app = Flask(__name__)


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/my_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)

# Create all tables
with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return 'Hello World!'


#USER
# Route to get all users (GET request)
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.as_dict() for user in users])

# Route to add a new user (POST request)
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        code=data['code'],
        profile=data['profile'],
        name=data['name'],
        gender=data['gender'],
        role=data['role'],
        email=data['email'],
        phone=data['phone'],
        address=data['address']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.as_dict()), 201

# Route to update a user (PUT request)
@app.route('/api/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)

    user.code = data['code']
    user.profile = data['profile']
    user.name = data['name']
    user.gender = data['gender']
    user.role = data['role']
    user.email = data['email']
    user.phone = data['phone']
    user.address = data['address']

    db.session.commit()
    return jsonify(user.as_dict())

# Route to delete a user (DELETE request)
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

@app.route('/admin/delete_user/<int:id>', methods=['POST'])
def admin_delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('adminuser'))


# CATEGORY
# Get all categories
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories]), 200
# @app.route('/api/categories', methods=['GET'])
# def get_categories():
#     categories = Category.query.all()
#     return jsonify([category.to_dict() for category in categories]), 200


# Create a new category
@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json()

    if not data or not data.get('name'):
        return jsonify({'error': 'Category name is required'}), 400

    new_category = Category(name=data['name'], description=data.get('description', ''))

    try:
        db.session.add(new_category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    return jsonify(new_category.to_dict()), 201


# Update an existing category
@app.route('/api/categories/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.get_json()
    category = Category.query.get_or_404(id)

    category.name = data['name']
    category.description = data.get('description', category.description)

    db.session.commit()

    return jsonify(category.to_dict()), 200


# Delete a category
@app.route('/api/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()

    return jsonify({'message': 'Category deleted successfully'}), 200


# PRODUCTS

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200


@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    # Validate required fields
    if not data.get('code') or not data.get('name') or not data.get('category_id'):
        return jsonify({'error': 'Code, name, and category_id are required'}), 400

    category = Category.query.get(data['category_id'])
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    new_product = Product(
        code=data['code'],
        name=data['name'],
        category=category,
        cost=data.get('cost', 0),
        price=data.get('price', 0),
        current_stock=data.get('current_stock', 0)
    )

    try:
        db.session.add(new_product)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    return jsonify(new_product.to_dict()), 201


@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)

    category = Category.query.get(data['category_id'])
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    product.code = data['code']
    product.name = data['name']
    product.category = category
    product.cost = data.get('cost', product.cost)
    product.price = data.get('price', product.price)
    product.current_stock = data.get('current_stock', product.current_stock)

    db.session.commit()
    return jsonify(product.to_dict()), 200


@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200


# ADMIN
@app.route('/admin')
def admin():
    module = 'index'
    return render_template("admin/index.html", module=module)

@app.route('/admin/category', methods=['GET', 'POST'])
def admincategory():
    module = 'category'
    return render_template("admin/category.html", module=module)

@app.route('/admin/product', methods=['GET', 'POST'])
def adminproduct():
    module = 'product'
    return render_template("admin/product.html", module=module)

@app.route('/admin/user', methods=['GET', 'POST'])
def adminuser():
    module = 'user'
    return render_template("admin/ai_user.html", module=module, )
    # return render_template("admin/user.html", module=module, item=item)


if __name__ == '__main__':
    app.run(debug=True)
