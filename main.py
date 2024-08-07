from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import requests


# Initialize Firebase Admin SDK
cred = credentials.Certificate("rhydhamfastapi.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = FastAPI()


@app.get("/hello")
def read_root():
    return {"message": "Hello World"}


@app.get("/add")
def add_date():
    # Get the current datetime
    now = datetime.now()
    day_of_week = now.strftime("%A")
    day_of_month = now.day
    month = now.strftime("%b")

    # Define the data to store
    data = {"Day of Week": day_of_week, "Day of Month": day_of_month, "Month": month}

    # Add a new document to the Firestore collection
    db.collection("sigaram_test_collection").add(data)

    return {"message": "Data added successfully", "data": data}


FAKE_STORE_BASE_URL = "https://fakestoreapi.com"


# Model for adding CartItem and ProductItem
class CartItem(BaseModel):
    userId: int
    productId: int
    quantity: int


class Product(BaseModel):
    title: str
    price: int
    description: str
    image: str
    category: str


@app.get("/get-all-products")
def list_all_products():
    response = requests.get(f"{FAKE_STORE_BASE_URL}/products")
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error fetching products"
        )
    return response.json()


@app.post("/add-to-cart")
def add_to_cart(item: CartItem):
    payload = {
        "userId": item.userId,
        "date": datetime.today().strftime("%Y-%m-%d"),
        "products": [{"productId": item.productId, "quantity": item.quantity}],
    }
    response = requests.post(f"{FAKE_STORE_BASE_URL}/carts", json=payload)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error adding item to cart"
        )
    return response.json()


@app.post("/add-product")
def add_to_cart(item: Product):
    payload = {
        "title": item.title,
        "price": item.price,
        "description": item.description,
        "image": item.image,
        "category": item.category,
    }
    response = requests.post(f"{FAKE_STORE_BASE_URL}/products", json=payload)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error adding item to cart"
        )
    return response.json()


@app.get("/cart-items/{user_id}")
def list_cart_items(user_id: int):
    response = requests.get(f"{FAKE_STORE_BASE_URL}/carts/user/{user_id}")
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error fetching cart items"
        )
    return response.json()


@app.delete("/delete-cart/{user_id}")
def delete_cart(user_id: int):
    response = requests.delete(f"{FAKE_STORE_BASE_URL}/carts/{user_id}")

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail="Error fetching cart items"
        )
    return response.json()


# To run the server, use the following command in the terminal:
# uvicorn main:app --reload
# or
# fastapi dev main.py
