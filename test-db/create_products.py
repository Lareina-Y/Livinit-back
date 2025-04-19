import json
import random

# Define possible styles, brands, and furniture types
styles = ["minimalist", "artdeco", "bohemian"]
brands = [
    "Meridian Furniture", "1st Dibs", "Lowe's", "Home Depot", "Wayfair", "Ikea",
    "My Bobs", "TOV Furniture", "Walmart", "Rove Concepts", "Ferm Living"
]
types = [
    "sofa", "coffee table", "tv stand", "bookshelf", "desk", "armchair",
    "dining table", "bed frame", "nightstand", "dresser"
]

# Generate realistic random dimensions for a furniture item
def random_dimensions():
    return {
        "width": round(random.uniform(30, 80), 1),
        "height": round(random.uniform(15, 50), 1),
        "depth": round(random.uniform(20, 40), 1)
    }

# Generate a product name based on type and brand with descriptive adjectives and materials
def generate_name(type_, brand):
    adjectives = ["Elegant", "Modern", "Vintage", "Classic", "Compact", "Deluxe"]
    materials = ["Wood", "Marble", "Metal", "Glass", "Velvet", "Leather"]
    return f"{random.choice(adjectives)} {random.choice(materials)} {type_.title()} by {brand}"

# Generate 200 unique products with varying attributes
products = []
for i in range(2000):  # Product IDs from 2000 to 2199
    product_type = random.choice(types)
    brand = random.choice(brands)
    style = random.choice(styles)
    product = {
        "id": i + 1,
        "name": generate_name(product_type, brand),
        "type": product_type,
        "price": round(random.uniform(49.99, 1499.99), 2),
        "brand": brand,
        "style": style,
        "dimensions": random_dimensions()
    }
    products.append(product)

# Export product list to a JSON string with indentation
products_json = json.dumps(products, indent=2)

# Save the generated JSON data to test_products.json
file_path = "test_products.json"
with open(file_path, "w") as f:
    f.write(products_json)
