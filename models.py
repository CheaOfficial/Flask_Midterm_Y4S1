from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    profile = db.Column(db.String(255))  # Path to profile image
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)

    def as_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'profile': self.profile,
            'name': self.name,
            'gender': self.gender,
            'role': self.role,
            'email': self.email,
            'phone': self.phone,
            'address': self.address
        }

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    current_stock = db.Column(db.Integer, nullable=False)
    category = db.relationship('Category', backref=db.backref('products', lazy=True))

    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'code': self.code,
    #         'name': self.name,
    #         'category': self.category.name,
    #         'cost': self.cost,
    #         'price': self.price,
    #         'current_stock': self.current_stock
    #     }
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None,  # Include the category name
            'cost': self.cost,
            'price': self.price,
            'current_stock': self.current_stock
        }
