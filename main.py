from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
import firebase_admin
import json
import re
import os

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FIREBASE_TEST_DB_NAME = os.getenv("FIREBASE_TEST_DB_NAME")

# Set OpenAI API key from environment variable
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Firebase Admin SDK with service account key
cred = credentials.Certificate("firebase-key.json")  # Path to your Firebase service account key
app = firebase_admin.initialize_app(cred, name='test-app')
db = firestore.client(app=app, database_id=FIREBASE_TEST_DB_NAME)

# Initialize FastAPI app
app = FastAPI()

# Define request body structure
class RecommendRequest(BaseModel):
    style: str        # e.g., "modern", "minimalist"
    budget: float     # max price user is willing to pay
    prompt: str       # description of desired room feel or purpose

# Define POST endpoint for product recommendation
@app.post("/recommend")
async def recommend(req: RecommendRequest):
    # Retrieve all products from Firebase Database
    products_ref = db.collection("Product")
    docs = products_ref.stream()
    all_products = [doc.to_dict() for doc in docs]

    if not all_products:
        return {"error": "No products found in the database."}

    # Filter products based on budget and selected style
    filtered = [
        product for product in all_products
        if product.get('price', 0) <= req.budget and req.style.lower() in product.get('style', '').lower()
    ]

    if not filtered:
        return {"recommendations": "No products match the given style and budget."}

    filtered = filtered[:100] # First 100 items

    # Compose prompt for OpenAI
    ai_prompt = f"""
    The user wants a room with a "{req.style}" style, a budget of ${req.budget} , and describes the goal as: {req.prompt}.
    Here is a list of filtered products (each with name, price, brand, style, type, dimensions):

    {filtered}

    Please recommend the best-fitting products (grouped by type), include "id", "name", and 1-2 sentence "reason" why each is a good match.
    Return the result strictly in JSON format.
    """

    # Query OpenAI to generate personalized recommendations
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=ai_prompt
        )

        # Step 1: Extract the actual JSON inside the triple backticks
        raw_string = response.output_text
        json_str = re.search(r"```json\n(.*)```", raw_string, re.DOTALL).group(1)

        # Step 2: Load the JSON string as a Python dictionary
        recommendations_dict = json.loads(json_str)

        return {"recommendations": recommendations_dict}
    except Exception as e:
        return {"error": str(e)}
