from pydantic import BaseModel, EmailStr, validator
from typing import List
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    password_hash: str
    email: EmailStr
    full_name: str | None = None
    registration_date: datetime
    is_active: bool = True
    roles: List[str] = []

class ProductCategory(BaseModel):
    id: int
    name: str
    description: str


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int

    @validator("price")
    def validate_price(cls, value):
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value

    @validator("stock_quantity")
    def validate_stock_quantity(cls, value):
        if value < 0:
            raise ValueError("Stock quantity cannot be negative")
        return value


class CartItem(BaseModel):
    product_id: int
    quantity: int

    @validator("quantity")
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError("Quantity must be greater than 0")
        return value

class CartResponse(BaseModel):
    item_id: int
    product_id: int
    product_name: str
    quantity: int
    total_price: float

class WishlistItem(BaseModel):
    user_id: int
    product_id: int

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    order_id: int
    user_id: int
    items: List[OrderItem]
    order_date: datetime
    total_amount: float
    status: str

class Payment(BaseModel):
    payment_id: int
    order_id: int
    payment_date: datetime
    payment_amount: float
    payment_status: str

class Review(BaseModel):
    user_id: int
    entity_id: int
    text: str
    created_at: datetime = datetime.now()

class Rating(BaseModel):
    user_id: int
    entity_id: int
    rating: int
    created_at: datetime = datetime.now()