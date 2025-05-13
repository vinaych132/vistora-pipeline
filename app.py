from flask import Flask, render_template, session, redirect, url_for, request, flash, jsonify

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

# Home route
@app.route('/')
def home():
    return render_template('home.html', cart_data=session.get('cart', []))

# Category route to display products based on category
@app.route('/category/<category_name>')
def category(category_name):
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

# Add item to cart
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
            item['size'] = 'M'  # Default size
            cart_data.append(item)
        session['cart'] = cart_data
    return redirect(url_for('cart'))

# Cart page to show added items
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_data = session.get('cart', [])
    coupon_discount = 0
    shipping_charge = 0

    if request.method == 'POST':
        if 'coupon_code' in request.form:
            coupon = request.form['coupon_code'].strip().upper()
            if coupon == 'SAVE100':
                session['coupon'] = 'SAVE100'

    total_price = sum(item['price'] * item['quantity'] for item in cart_data)

    if session.get('coupon') == 'SAVE100':
        coupon_discount = 100

    if total_price < 1000 and total_price > 0:
        shipping_charge = 50

    grand_total = total_price + shipping_charge - coupon_discount

    return render_template(
        'cart.html',
        cart_data=cart_data,
        total_price=total_price,
        coupon_discount=coupon_discount,
        shipping_charge=shipping_charge,
        grand_total=grand_total,
        coupon=session.get('coupon', ''),
        shipping_estimate=session.get('shipping_estimate', '')
    )

# Update quantity of item in cart
@app.route('/update_quantity/<item_name>/<action>', methods=['POST'])
def update_quantity(item_name, action):
    cart_data = session.get('cart', [])
    for item in cart_data:
        if item['name'] == item_name:
            if action == 'increment':
                item['quantity'] += 1
            elif action == 'decrement' and item['quantity'] > 1:
                item['quantity'] -= 1
            break
    session['cart'] = cart_data
    return redirect(url_for('cart'))

# Update size of item in cart
@app.route('/update_size', methods=['POST'])
def update_size():
    data = request.get_json()
    item_name = data.get('item_name')
    new_size = data.get('new_size')

    for item in session.get('cart', []):
        if item['name'] == item_name:
            item['size'] = new_size
            break

    session.modified = True
    return jsonify({'success': True})

# Estimate shipping cost based on pincode
@app.route('/estimate_shipping', methods=['POST'])
def estimate_shipping():
    pincode = request.form.get('pincode')

    if pincode and pincode.startswith("5"):
        estimate = "₹50 - Delivery in 2-4 days"
    else:
        estimate = "₹80 - Delivery in 4-6 days"

    session['shipping_estimate'] = estimate
    return redirect(url_for('cart'))

# Remove item from cart
@app.route('/remove_from_cart/<item_name>', methods=['POST'])
def remove_from_cart(item_name):
    cart_data = session.get('cart', [])
    cart_data = [item for item in cart_data if item['name'] != item_name]
    session['cart'] = cart_data
    return redirect(url_for('cart'))

# Clear all items from cart
@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    session.pop('coupon', None)
    session.pop('shipping_estimate', None)
    return redirect(url_for('cart'))

# Billing page to show payment options
@app.route('/billing')
@app.route('/checkout')
def billing():
    cart_data = session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart_data)
    return render_template('billing.html', cart_data=cart_data, total_price=total_price)

# Apply coupon to cart
@app.route('/apply_coupon', methods=['POST'])
def apply_coupon():
    coupon_code = request.form.get('coupon_code')
    if coupon_code == 'SAVE100':
        session['coupon'] = 'SAVE100'
        flash(f"Coupon {coupon_code} applied successfully!", 'success')
    else:
        flash('Invalid coupon code.', 'danger')
    return redirect(url_for('cart'))

# Main entry point to run the app
if __name__ == '__main__':
    app.run(debug=True)
