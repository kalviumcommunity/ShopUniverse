from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from abc import ABC, abstractmethod

class User(BaseModel):
    user_id: int
    username: str
    password_hash: str
    email: EmailStr
    full_name: str | None = None
    registration_date: datetime
    is_active: bool = True
    roles: str = 'Customer'
    address: str | None = None
    phone_number: str | None = None
    date_of_birth: datetime | None = None



class ProductCategory(BaseModel):
    category_id: int
    name: str
    description: str

    def __init__(self, **data):
        super().__init__(**data)  
        print(f" {self.name} category is being added")


class Product(BaseModel):
    product_id: int
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int
    manufacturer: str | None = None
    weight: float | None = None
    is_available: bool = True
    image_url: str | None = None
    MIN_PRODUCT_QUANTITY:int = 1
    MAX_PRODUCT_QUANTITY:int  = 10000

    def __init__(self, **data):
        super().__init__(**data)  
        print(f" {self.name} product is being added")

class CartItem(BaseModel):
    cart_item_id: int
    quantity: int
    product_id: int  
    cart_id: int  
    MIN_QUANTITY:int = 1

class Cart(BaseModel):
    cart_id: int
    user_id: int  

class WishlistItem(BaseModel):
    wishlist_item_id: int
    user_id: int 
    product_id: int 


class OrderItem(BaseModel):
    order_item_id: int
    quantity: int
    product_id: int 
    order_id: int 
    MIN_ORDER:int = 1

    def __init__(self, **data):
        super().__init__(**data)  
        print(f"User {self.name} category is being added")

class Order(BaseModel):
    order_id: int
    user_id: int

    def __del__(self):
        print(f"order {self.order_id} is being completted")

class Payment(BaseModel):
    payment_id: int
    order_id: int  


