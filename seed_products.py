from app import app, db, Product  # Make sure Product is imported from app.py

# Define your products
products = [
    {
        "name": "Classic Tee",
        "price": 499,
        "image": "tshirt.jpg",
        "sizes": ["S", "M", "L"],
        "stock": {"S": 10, "M": 8, "L": 5}
    },
    {
        "name": "V-Neck Tee",
        "price": 599,
        "image": "tshirt2.jpg",
        "sizes": ["M", "L", "XL"],
        "stock": {"M": 6, "L": 7, "XL": 4}
    },
    {
        "name": "Slim Trackpant",
        "price": 799,
        "image": "trackpant.jpg",
        "sizes": ["S", "M", "L", "XL"],
        "stock": {"S": 5, "M": 10, "L": 7, "XL": 3}
    },
    {
        "name": "Sport Trackpant",
        "price": 899,
        "image": "trackpant2.jpg",
        "sizes": ["M", "L"],
        "stock": {"M": 9, "L": 5}
    },
    {
        "name": "Basic Cap",
        "price": 299,
        "image": "cap1.jpg",
        "sizes": ["Free"],
        "stock": {"Free": 20}
    },
    {
        "name": "Snapback Cap",
        "price": 399,
        "image": "cap2.jpg",
        "sizes": ["Free"],
        "stock": {"Free": 15}
    },
    {
        "name": "Classic Hoodie",
        "price": 999,
        "image": "hoodie.jpg",
        "sizes": ["M", "L", "XL"],
        "stock": {"M": 4, "L": 6, "XL": 3}
    },
    {
        "name": "Zipped Hoodie",
        "price": 1199,
        "image": "hoodie2.jpg",
        "sizes": ["S", "M", "L"],
        "stock": {"S": 2, "M": 5, "L": 5}
    },
    {
        "name": "Cotton Briefs",
        "price": 199,
        "image": "underwear.jpg",
        "sizes": ["M", "L"],
        "stock": {"M": 10, "L": 10}
    },
    {
        "name": "Boxer Shorts",
        "price": 299,
        "image": "underwear2.jpg",
        "sizes": ["L", "XL"],
        "stock": {"L": 7, "XL": 6}
    }
]

# Seed inside app context
with app.app_context():
    for item in products:
        product = Product(
            name=item["name"],
            price=item["price"],
            image=item["image"],
            sizes=item["sizes"],
            stock=item["stock"]
        )
        db.session.add(product)

    db.session.commit()
    print("✅ Products seeded successfully.")
