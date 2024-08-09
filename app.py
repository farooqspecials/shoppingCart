from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Category model
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    products = db.relationship('Product', backref='category', lazy=True)

# Define the Product model with a price field
class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)  # Add a price field
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

#home page 
@app.route('/')
def home():
    return render_template('home.html')

# Route for adding categories
@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        category_name = request.form['name']
        # Check if the category already exists
        existing_category = Category.query.filter_by(name=category_name).first()
        if existing_category is None:
            new_category = Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()
            return redirect(url_for('add_category'))
        else:
            return "Category already exists!", 400
    return render_template('add_category.html')

# Route for adding products
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    categories = Category.query.all()
    if request.method == 'POST':
        product_name = request.form['name']
        product_price = request.form['price']
        category_id = request.form['category_id']
        
        try:
            # Convert price to a float
            product_price = float(product_price)
        except ValueError:
            return "Invalid price! Please enter a valid number.", 400
        
        # Check if the product name and category are provided
        if product_name and category_id:
            new_product = Product(name=product_name, price=product_price, category_id=category_id)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('add_product'))
        else:
            return "Product name, price, and category are required!", 400

    return render_template('add_product.html', categories=categories)


# Route to list all categories
@app.route('/categories')
def list_categories():
    # Query all categories
    categories = Category.query.all()
    return render_template('list_categories.html', categories=categories)

# Route to list all products with their categories using an explicit join
@app.route('/products_and_categories')
def list_products_and_categories():
    # Perform a join between Product and Category
    products_with_categories = db.session.query(Product, Category).join(Category).all()

    return render_template('list_products_and_categories.html', products_with_categories=products_with_categories)


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
