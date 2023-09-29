# main.py
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime
from model import User, Product,ProductCategory,CartItem,CartResponse,WishlistItem,Order,OrderItem,Payment,Rating,Review

app = FastAPI()


users_db = []
product_categories_db = []
products_db = []
cart_db = []
wishlist_db = []
orders_db = []
payments_db = []
reviews_db = []
ratings_db = []
next_order_id = 1
next_payment_id = 1
product_db = {
    1: {"name": "Product 1", "price": 10.0},
    2: {"name": "Product 2", "price": 20.0},
}



# Create a new user
@app.post("/users/", response_model=User)
async def create_user(user: User):
    users_db.append(user)
    return user

# Get a user by ID
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Get all users
@app.get("/users/", response_model=List[User])
async def get_all_users():
    return users_db

# Update a user by ID
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, updated_user: User):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            users_db[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# Delete a user by ID
@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if user.id == user_id:
            deleted_user = users_db.pop(i)
            return deleted_user
    raise HTTPException(status_code=404, detail="User not found")

# Create a new ProductCategory
@app.post("/product_categories/", response_model=ProductCategory)
async def create_product_category(category: ProductCategory):
    product_categories_db.append(category)
    return category

# Get a ProductCategory by ID
@app.get("/product_categories/{category_id}", response_model=ProductCategory)
async def get_product_category(category_id: int):
    for category in product_categories_db:
        if category.id == category_id:
            return category
    raise HTTPException(status_code=404, detail="Product Category not found")

# Get all ProductCategories
@app.get("/product_categories/", response_model=List[ProductCategory])
async def get_all_product_categories():
    return product_categories_db

# Create a new Product
@app.post("/products/", response_model=Product)
async def create_product(product: Product):
    products_db.append(product)
    return product

# Get a Product by ID
@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    for product in products_db:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

# Get all Products
@app.get("/products/", response_model=List[Product])
async def get_all_products():
    return products_db

# Route to add an item to the shopping cart
@app.post("/add-to-cart/", response_model=CartResponse)
async def add_to_cart(item: CartItem):
    product = product_db.get(item.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    total_price = product["price"] * item.quantity
    cart_item = {
        "item_id": len(cart_db) + 1,
        "product_id": item.product_id,
        "product_name": product["name"],
        "quantity": item.quantity,
        "total_price": total_price,
    }
    cart_db.append(cart_item)
    return cart_item

# Route to view the contents of the shopping cart
@app.get("/view-cart/", response_model=List[CartResponse])
async def view_cart():
    return cart_db

# Route to update the quantity of an item in the cart
@app.put("/update-cart/{item_id}/", response_model=CartResponse)
async def update_cart_item(item_id: int, quantity: int):
    for item in cart_db:
        if item["item_id"] == item_id:
            product = product_db.get(item["product_id"])
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            item["quantity"] = quantity
            item["total_price"] = product["price"] * quantity
            return item
    raise HTTPException(status_code=404, detail="Item not found in cart")

# Route to remove an item from the cart
@app.delete("/remove-from-cart/{item_id}/", response_model=CartResponse)
async def remove_from_cart(item_id: int):
    for item in cart_db:
        if item["item_id"] == item_id:
            cart_db.remove(item)
            return item
    raise HTTPException(status_code=404, detail="Item not found in cart")

@app.post("/add-to-wishlist/", response_model=WishlistItem)
async def add_to_wishlist(item: WishlistItem):
    # Check if the user and product exist
    if item.user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be greater than 0")
    if item.product_id not in product_db:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if the item is already in the wishlist
    for existing_item in wishlist_db:
        if existing_item.user_id == item.user_id and existing_item.product_id == item.product_id:
            raise HTTPException(status_code=400, detail="Item is already in the wishlist")

    wishlist_db.append(item)
    return item

# Route to view the user's wishlist
@app.get("/view-wishlist/{user_id}", response_model=List[WishlistItem])
async def view_wishlist(user_id: int):
    user_wishlist = [item for item in wishlist_db if item.user_id == user_id]
    return user_wishlist


# Route to remove an item from the wishlist
@app.delete("/remove-from-wishlist/{user_id}/{product_id}", response_model=WishlistItem)
async def remove_from_wishlist(user_id: int, product_id: int):
    # Check if the user and product exist
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="User ID must be greater than 0")
    if product_id not in product_db:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if the item is in the wishlist
    removed_item = None
    for item in wishlist_db:
        if item.user_id == user_id and item.product_id == product_id:
            removed_item = item
            wishlist_db.remove(item)
            break

    if removed_item is None:
        raise HTTPException(status_code=404, detail="Item not found in the wishlist")

    return removed_item

# Route to create an order
@app.post("/create-order/", response_model=Order)
async def create_order(order: Order):
    global next_order_id
    order.order_id = next_order_id
    next_order_id += 1
    order.order_date = datetime.now()
    orders_db.append(order)
    return order

# Route to create a payment
@app.post("/create-payment/", response_model=Payment)
async def create_payment(payment: Payment):
    global next_payment_id
    payment.payment_id = next_payment_id
    next_payment_id += 1
    payment.payment_date = datetime.now()
    
    # Check if the associated order exists
    associated_order = next((order for order in orders_db if order.order_id == payment.order_id), None)
    if not associated_order:
        raise HTTPException(status_code=404, detail="Associated order not found")

    payments_db.append(payment)
    return payment

# Route to get a specific order by ID
@app.get("/get-order/{order_id}", response_model=Order)
async def get_order(order_id: int):
    order = next((order for order in orders_db if order.order_id == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Route to get a specific payment by ID
@app.get("/get-payment/{payment_id}", response_model=Payment)
async def get_payment(payment_id: int):
    payment = next((payment for payment in payments_db if payment.payment_id == payment_id), None)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# Route to list all orders
@app.get("/list-orders/", response_model=List[Order])
async def list_orders():
    return orders_db

# Route to list all payments
@app.get("/list-payments/", response_model=List[Payment])
async def list_payments():
    return payments_db


# Route to create a review
@app.post("/create-review/", response_model=Review)
async def create_review(review: Review):
    
    if not entity_exists(review.entity_id):
        raise HTTPException(status_code=404, detail="Entity not found")


    review.created_at = datetime.now()
    reviews_db.append(review)
    return review

# Route to create a rating
@app.post("/create-rating/", response_model=Rating)
async def create_rating(rating: Rating):
   
    if not entity_exists(rating.entity_id):
        raise HTTPException(status_code=404, detail="Entity not found")

    
    if not (1 <= rating.rating <= 5):
        raise HTTPException(status_code=400, detail="Invalid rating value")

   
    rating.created_at = datetime.now()
    ratings_db.append(rating)
    return rating

# Route to get reviews for a specific entity by entity ID
@app.get("/get-reviews/{entity_id}", response_model=List[Review])
async def get_reviews(entity_id: int):
    entity_reviews = [review for review in reviews_db if review.entity_id == entity_id]
    return entity_reviews


@app.get("/get-ratings/{entity_id}", response_model=List[Rating])
async def get_ratings(entity_id: int):
    entity_ratings = [rating for rating in ratings_db if rating.entity_id == entity_id]
    return entity_ratings


def entity_exists(entity_id):
   return entity_id in [1, 2, 3] 