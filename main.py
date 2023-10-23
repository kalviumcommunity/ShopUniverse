# main.py
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime
from model import User, Product, Payment, ProductCategory, Rating, Review, Cart, CartItem, WishlistItem, OrderItem, Order

app = FastAPI()

users_db = []
categories_db = []
products_db = []
carts_db = []
wishlist_items_db = []
order_items_db = []
orders_db = []
payments_db = []
reviews_db = []
ratings_db = []
product_lists_db = []
cart_items_db = []

# Create, Read, Update, Delete User
@app.post("/users/", response_model=User)
def create_user(user: User):
    # print()
    user.user_id = len(users_db) + 1
    users_db.append(user)
    return user

@app.get("/users/{user_id}/", response_model=User)
def get_user(user_id: int):
    for user in users_db:
        if user.user_id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}/", response_model=User)
def update_user(user_id: int, updated_user: User):
    for i, user in enumerate(users_db):
        if user.user_id == user_id:
            users_db[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}/", response_model=User)
def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if user.user_id == user_id:
            deleted_user = users_db.pop(i)
            return deleted_user
    raise HTTPException(status_code=404, detail="User not found")

# Create, Read, Update, Delete Category
@app.post("/categories/", response_model=ProductCategory)
def create_category(category: ProductCategory):
    category.category_id = len(categories_db) + 1
    categories_db.append(category)
    return category

@app.get("/categories/{category_id}/", response_model=ProductCategory)
def get_category(category_id: int):
    for category in categories_db:
        if category.category_id == category_id:
            return category
    raise HTTPException(status_code=404, detail="Category not found")

@app.put("/categories/{category_id}/", response_model=ProductCategory)
def update_category(category_id: int, updated_category: ProductCategory):
    for i, category in enumerate(categories_db):
        if category.category_id == category_id:
            categories_db[i] = updated_category
            return updated_category
    raise HTTPException(status_code=404, detail="Category not found")

@app.delete("/categories/{category_id}/", response_model=ProductCategory)
def delete_category(category_id: int):
    for i, category in enumerate(categories_db):
        if category.category_id == category_id:
            deleted_category = categories_db.pop(i)
            return deleted_category
    raise HTTPException(status_code=404, detail="Category not found")

# Create, Read, Update, Delete Product
@app.post("/products/", response_model=Product)
def create_product(product: Product):
    product.product_id = len(products_db) + 1
    
    category = next((cat for cat in categories_db if cat.category_id == product.category_id), None)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    products_db.append(product)
    return product

@app.get("/categories/{category_id}/products/", response_model=List[Product])
def get_products_by_category(category_id: int):
    category = next((cat for cat in categories_db if cat.category_id == category_id), None)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category_products = [product for product in products_db if product.category_id == category_id]
    
    return category_products

# Create, Read, Update, Delete Cart
@app.post("/carts/", response_model=Cart)
def create_cart(cart: Cart):
    cart.cart_id = len(carts_db) + 1
    carts_db.append(cart)
    return cart

@app.get("/carts/{cart_id}/", response_model=Cart)
def get_cart(cart_id: int):
    for cart in carts_db:
        if cart.cart_id == cart_id:
            return cart
    raise HTTPException(status_code=404, detail="Cart not found")

@app.put("/carts/{cart_id}/", response_model=Cart)
def update_cart(cart_id: int, updated_cart: Cart):
    for i, cart in enumerate(carts_db):
        if cart.cart_id == cart_id:
            carts_db[i] = updated_cart
            return updated_cart
    raise HTTPException(status_code=404, detail="Cart not found")

@app.delete("/carts/{cart_id}/", response_model=Cart)
def delete_cart(cart_id: int):
    for i, cart in enumerate(carts_db):
        if cart.cart_id == cart_id:
            deleted_cart = carts_db.pop(i)
            return deleted_cart
    raise HTTPException(status_code=404, detail="Cart not found")

# Create, Read, Update, Delete CartItem
@app.post("/cartitems/", response_model=CartItem)
def create_cart_item(cart_item: CartItem):
    cart_item.cart_item_id = len(cart_items_db) + 1
    product = next((prod for prod in products_db if prod.product_id == cart_item.product.product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    cart = next((crt for crt in carts_db if crt.cart_id == cart_item.cart.cart_id), None)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    cart_items_db.append(cart_item)
    return cart_item

@app.get("/cartitems/{cart_item_id}/", response_model=CartItem)
def get_cart_item(cart_item_id: int):
    for cart_item in cart_items_db:
        if cart_item.cart_item_id == cart_item_id:
            return cart_item
    raise HTTPException(status_code=404, detail="Cart item not found")

@app.put("/cartitems/{cart_item_id}/", response_model=CartItem)
def update_cart_item(cart_item_id: int, updated_cart_item: CartItem):
    for i, cart_item in enumerate(cart_items_db):
        if cart_item.cart_item_id == cart_item_id:
            cart_items_db[i] = updated_cart_item
            return updated_cart_item
    raise HTTPException(status_code=404, detail="Cart item not found")

@app.delete("/cartitems/{cart_item_id}/", response_model=CartItem)
def delete_cart_item(cart_item_id: int):
    for i, cart_item in enumerate(cart_items_db):
        if cart_item.cart_item_id == cart_item_id:
            deleted_cart_item = cart_items_db.pop(i)
            return deleted_cart_item
    raise HTTPException(status_code=404, detail="Cart item not found")

# Create, Read, Update, Delete WishlistItem
@app.post("/wishlists/", response_model=WishlistItem)
def create_wishlist_item(wishlist_item: WishlistItem):
    wishlist_item.wishlist_item_id = len(wishlist_items_db) + 1
    user = next((usr for usr in users_db if usr.user_id == wishlist_item.user.user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    product = next((prod for prod in products_db if prod.product_id == wishlist_item.product.product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    wishlist_items_db.append(wishlist_item)
    return wishlist_item

@app.get("/wishlists/{wishlist_item_id}/", response_model=WishlistItem)
def get_wishlist_item(wishlist_item_id: int):
    for wishlist_item in wishlist_items_db:
        if wishlist_item.wishlist_item_id == wishlist_item_id:
            return wishlist_item
    raise HTTPException(status_code=404, detail="Wishlist item not found")

@app.put("/wishlists/{wishlist_item_id}/", response_model=WishlistItem)
def update_wishlist_item(wishlist_item_id: int, updated_wishlist_item: WishlistItem):
    for i, wishlist_item in enumerate(wishlist_items_db):
        if wishlist_item.wishlist_item_id == wishlist_item_id:
            wishlist_items_db[i] = updated_wishlist_item
            return updated_wishlist_item
    raise HTTPException(status_code=404, detail="Wishlist item not found")

@app.delete("/wishlists/{wishlist_item_id}/", response_model=WishlistItem)
def delete_wishlist_item(wishlist_item_id: int):
    for i, wishlist_item in enumerate(wishlist_items_db):
        if wishlist_item.wishlist_item_id == wishlist_item_id:
            deleted_wishlist_item = wishlist_items_db.pop(i)
            return deleted_wishlist_item
    raise HTTPException(status_code=404, detail="Wishlist item not found")

# Create, Read, Update, Delete OrderItem
@app.post("/orderitems/", response_model=OrderItem)
def create_order_item(order_item: OrderItem):
    order_item.order_item_id = len(order_items_db) + 1
    product = next((prod for prod in products_db if prod.product_id == order_item.product.product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    order = next((ordr for ordr in orders_db if ordr.order_id == order_item.order.order_id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order_items_db.append(order_item)
    return order_item

@app.get("/orderitems/{order_item_id}/", response_model=OrderItem)
def get_order_item(order_item_id: int):
    for order_item in order_items_db:
        if order_item.order_item_id == order_item_id:
            return order_item
    raise HTTPException(status_code=404, detail="Order item not found")

@app.put("/orderitems/{order_item_id}/", response_model=OrderItem)
def update_order_item(order_item_id: int, updated_order_item: OrderItem):
    for i, order_item in enumerate(order_items_db):
        if order_item.order_item_id == order_item_id:
            order_items_db[i] = updated_order_item
            return updated_order_item
    raise HTTPException(status_code=404, detail="Order item not found")

@app.delete("/orderitems/{order_item_id}/", response_model=OrderItem)
def delete_order_item(order_item_id: int):
    for i, order_item in enumerate(order_items_db):
        if order_item.order_item_id == order_item_id:
            deleted_order_item = order_items_db.pop(i)
            return deleted_order_item
    raise HTTPException(status_code=404, detail="Order item not found")

# Create, Read, Update, Delete Order
@app.post("/orders/", response_model=Order)
def create_order(order: Order):
    order.order_id = len(orders_db) + 1
    user = next((usr for usr in users_db if usr.user_id == order.user.user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    orders_db.append(order)
    return order

@app.get("/orders/{order_id}/", response_model=Order)
def get_order(order_id: int):
    for order in orders_db:
        if order.order_id == order_id:
            return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}/", response_model=Order)
def update_order(order_id: int, updated_order: Order):
    for i, order in enumerate(orders_db):
        if order.order_id == order_id:
            orders_db[i] = updated_order
            return updated_order
    raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/orders/{order_id}/", response_model=Order)
def delete_order(order_id: int):
    for i, order in enumerate(orders_db):
        if order.order_id == order_id:
            deleted_order = orders_db.pop(i)
            return deleted_order
    raise HTTPException(status_code=404, detail="Order not found")

# Create, Read, Update, Delete Payment
@app.post("/payments/", response_model=Payment)
def create_payment(payment: Payment):
    payment.payment_id = len(payments_db) + 1
    order = next((ordr for ordr in orders_db if ordr.order_id == payment.order.order_id), None)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    payments_db.append(payment)
    return payment

@app.get("/payments/{payment_id}/", response_model=Payment)
def get_payment(payment_id: int):
    for payment in payments_db:
        if payment.payment_id == payment_id:
            return payment
    raise HTTPException(status_code=404, detail="Payment not found")

@app.put("/payments/{payment_id}/", response_model=Payment)
def update_payment(payment_id: int, updated_payment: Payment):
    for i, payment in enumerate(payments_db):
        if payment.payment_id == payment_id:
            payments_db[i] = updated_payment
            return updated_payment
    raise HTTPException(status_code=404, detail="Payment not found")

@app.delete("/payments/{payment_id}/", response_model=Payment)
def delete_payment(payment_id: int):
    for i, payment in enumerate(payments_db):
        if payment.payment_id == payment_id:
            deleted_payment = payments_db.pop(i)
            return deleted_payment
    raise HTTPException(status_code=404, detail="Payment not found")

# Create, Read, Update, Delete Review
@app.post("/reviews/", response_model=Review)
def create_review(review: Review):
    review.review_id = len(reviews_db) + 1
    product = next((prod for prod in products_db if prod.product_id == review.product.product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    reviews_db.append(review)
    return review

@app.get("/reviews/{review_id}/", response_model=Review)
def get_review(review_id: int):
    for review in reviews_db:
        if review.review_id == review_id:
            return review
    raise HTTPException(status_code=404, detail="Review not found")

@app.put("/reviews/{review_id}/", response_model=Review)
def update_review(review_id: int, updated_review: Review):
    for i, review in enumerate(reviews_db):
        if review.review_id == review_id:
            reviews_db[i] = updated_review
            return updated_review
    raise HTTPException(status_code=404, detail="Review not found")

@app.delete("/reviews/{review_id}/", response_model=Review)
def delete_review(review_id: int):
    for i, review in enumerate(reviews_db):
        if review.review_id == review_id:
            deleted_review = reviews_db.pop(i)
            return deleted_review
    raise HTTPException(status_code=404, detail="Review not found")

# Create, Read, Update, Delete Rating
@app.post("/ratings/", response_model=Rating)
def create_rating(rating: Rating):
    rating.rating_id = len(ratings_db) + 1
    product = next((prod for prod in products_db if prod.product_id == rating.product.product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    ratings_db.append(rating)
    return rating

@app.get("/ratings/{rating_id}/", response_model=Rating)
def get_rating(rating_id: int):
    for rating in ratings_db:
        if rating.rating_id == rating_id:
            return rating
    raise HTTPException(status_code=404, detail="Rating not found")

@app.put("/ratings/{rating_id}/", response_model=Rating)
def update_rating(rating_id: int, updated_rating: Rating):
    for i, rating in enumerate(ratings_db):
        if rating.rating_id == rating_id:
            ratings_db[i] = updated_rating
            return updated_rating
    raise HTTPException(status_code=404, detail="Rating not found")

@app.delete("/ratings/{rating_id}/", response_model=Rating)
def delete_rating(rating_id: int):
    for i, rating in enumerate(ratings_db):
        if rating.rating_id == rating_id:
            deleted_rating = ratings_db.pop(i)
            return deleted_rating
    raise HTTPException(status_code=404, detail="Rating not found")

