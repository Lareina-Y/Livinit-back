from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
import firebase_admin
import os

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set OpenAI API key from environment variable
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Firebase Admin SDK with service account key
cred = credentials.Certificate("firebase-key.json")  # Path to your Firebase service account key
firebase_admin.initialize_app(cred)

db = firestore.client()

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

    # Compose prompt for OpenAI
    ai_prompt = f"""
    The user wants a room with a "{req.style}" style, a budget of ${req.budget} , and describes the goal as: {req.prompt}.
    Here is a list of filtered products (each with name, price, brand, style, type, dimensions):

    {filtered}

    Based on this, please list the product id and name of recommended items that best fit the user's preferences, and briefly explain why.
    """

    # Query OpenAI to generate personalized recommendations
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input=ai_prompt
        )
        return {"recommendations": response.output_text}
    except Exception as e:
        return {"error": str(e)}
