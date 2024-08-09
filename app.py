from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set the secret key to a random string
app.secret_key = 'xf5\xd8\xc1\x1f\xab\xde\x9a\x8d\xce\x92\x8c\xed\x03\xd4\x8e\xc6\x89\xff\xf1\xae\xbc\xde'  # Replace with a unique and secure key

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

#shopping cart logics
# Function to add product to cart
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    
    # Ensure product_id is stored as a string
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
    
    session['cart'] = cart


# Route to add product to cart
@app.route('/add_to_cart/<int:product_id>')
def add_product_to_cart(product_id):
    add_to_cart(product_id)
    return redirect(url_for('list_products_and_categories'))

# Route to view cart
@app.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    # Convert keys to integers for querying the database
    product_ids = map(int, cart.keys())
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    
    cart_items = []
    for product in products:
        product_id_str = str(product.id)  # Ensure the product ID is a string
        quantity = cart[product_id_str]
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })
    
    total_amount = sum(item['total_price'] for item in cart_items)
    
    return render_template('cart.html', cart_items=cart_items, total_amount=total_amount)


# Route to list all products with Add to Cart buttons
@app.route('/products_and_cart')
def list_products_and_cart():
    products_with_categories = db.session.query(Product, Category).join(Category).all()
    return render_template('list_products_and_cart.html', products_with_categories=products_with_categories)



# Run the application
if __name__ == '__main__':
    app.run(debug=True)
