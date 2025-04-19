import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import json
import os

# Load environment variables from .env file
load_dotenv()

FIREBASE_TEST_DB_NAME = os.getenv("FIREBASE_TEST_DB_NAME")

# Initialize Firestore
cred = credentials.Certificate("../firebase-key.json")
app = firebase_admin.initialize_app(cred, name='test-app')
db = firestore.client(app=app, database_id=FIREBASE_TEST_DB_NAME)  # Specify database name here

# Load the product data
with open("test_products.json", "r") as f:
    products = json.load(f)

# Add to Firestore collection named "test"
for product in products:
    doc_ref = db.collection("Product").document(str(product["id"]))
    doc_ref.set(product)

print(f"{len(products)} products uploaded to Firestore collection 'Product'.")