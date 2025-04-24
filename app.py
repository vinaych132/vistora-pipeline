from flask import Flask, render_template, session, redirect, url_for, request, Response

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'  # Required for session management

# 🔐 Password Gate Setup
USERNAME = "vistora"
PASSWORD = "secret123"  # Change this to your own secure password

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        "Authentication Required", 401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'})

@app.before_request
def require_auth():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
# Route to display products for a specific category
@app.route('/category/<category_name>')
def category(category_name):
    # Hardcoded products for the demo (can be dynamic from a database)
    products = {
        'tshirts': [
            {'name': 'Classic Tee', 'price': 499, 'image': 'tshirt.jpg'},
            {'name': 'V-Neck Tee', 'price': 599, 'image': 'tshirt2.jpg'}
        ],
        'trackpants': [
            {'name': 'Slim Trackpant', 'price': 799, 'image': 'trackpant.jpg'},
            {'name': 'Sport Trackpant', 'price': 899, 'image': 'trackpant2.jpg'}
        ],
        'caps': [
            {'name': 'Basic Cap', 'price': 299, 'image': 'cap1.jpg'},
            {'name': 'Snapback Cap', 'price': 399, 'image': 'cap2.jpg'}
        ],
        'hoodies': [
            {'name': 'Classic Hoodie', 'price': 999, 'image': 'hoodie.jpg'},
            {'name': 'Zipped Hoodie', 'price': 1199, 'image': 'hoodie2.jpg'}
        ],
        'underwear': [
            {'name': 'Cotton Briefs', 'price': 199, 'image': 'underwear.jpg'},
            {'name': 'Boxer Shorts', 'price': 299, 'image': 'underwear2.jpg'}
        ]
    }

    items = products.get(category_name, [])
    return render_template('category.html', category_name=category_name.capitalize(), items=items, cart_count=len(session.get('cart', [])))

# Home route
@app.route('/')
def home():
    return render_template('home.html', cart_data=session.get('cart', []))

# Cart Route - Displays the current cart
@app.route('/cart')
def cart():
    cart_data = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_data)
    return render_template('cart.html', cart_data=cart_data, total_price=total_price)

# Add to Cart Route
@app.route('/add_to_cart/<item_name>', methods=['POST'])
def add_to_cart(item_name):
    item_catalog = {
        'Classic Tee': {'name': 'Classic Tee', 'price': 499, 'image': 'tshirt.jpg'},
        'V-Neck Tee': {'name': 'V-Neck Tee', 'price': 599, 'image': 'tshirt2.jpg'},
        'Slim Trackpant': {'name': 'Slim Trackpant', 'price': 799, 'image': 'trackpant.jpg'},
        'Sport Trackpant': {'name': 'Sport Trackpant', 'price': 899, 'image': 'trackpant2.jpg'},
        'Basic Cap': {'name': 'Basic Cap', 'price': 299, 'image': 'cap1.jpg'},
        'Snapback Cap': {'name': 'Snapback Cap', 'price': 399, 'image': 'cap2.jpg'},
        'Classic Hoodie': {'name': 'Classic Hoodie', 'price': 999, 'image': 'hoodie.jpg'},
        'Zipped Hoodie': {'name': 'Zipped Hoodie', 'price': 1199, 'image': 'hoodie2.jpg'},
        'Cotton Briefs': {'name': 'Cotton Briefs', 'price': 199, 'image': 'underwear.jpg'},
        'Boxer Shorts': {'name': 'Boxer Shorts', 'price': 299, 'image': 'underwear2.jpg'}
    }

    item = item_catalog.get(item_name)

    if item:
        cart_data = session.get('cart', [])
        found = False
        for cart_item in cart_data:
            if cart_item['name'] == item['name']:
                cart_item['quantity'] += 1
                found = True
                break
        if not found:
            item['quantity'] = 1
            cart_data.append(item)

        session['cart'] = cart_data

    return redirect(url_for('cart'))

# Remove Item from Cart
@app.route('/remove_from_cart/<item_name>', methods=['POST'])
def remove_from_cart(item_name):
    cart_data = session.get('cart', [])
    cart_data = [item for item in cart_data if item['name'] != item_name]
    session['cart'] = cart_data
    return redirect(url_for('cart'))

# Clear Cart Route
@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))

# Billing / Checkout Route
@app.route('/billing')
@app.route('/checkout')
def billing():
    cart_data = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_data)
    return render_template('billing.html', cart_data=cart_data, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)