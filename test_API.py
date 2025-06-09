from app import utils
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SellerCreate(BaseModel):
    name: str
    avatar: str

class BuyerCreate(BaseModel):
    name: str

class ProductCreate(BaseModel):
    seller_id: int
    picture: str

class ProductInfoCreate(BaseModel):
    seller_id: int
    product_id: int
    info: str

class BalanceUpdate(BaseModel):
    id: int
    pay: int

@app.get("/seller/info")
def get_seller(id: int):
    """Работает"""
    return utils.get_seller(id)

@app.get("/seller/list")
def get_seller_from_pagination(offset: int = 0, fetch: int = 5):
    """Работает"""
    seller_list = []
    for id in range(offset, fetch+1):
        seller_list.append(utils.get_seller(id))
    return seller_list

@app.get("/buyer")
def get_buyer_from_id(id: int):
    """Работает"""
    return utils.get_buyer(id)

@app.get("/product")
def get_product(seller_id: int, product_id: int):
    """Работает"""
    return utils.get_product(seller_id, product_id)

@app.get("/product/info")
def get_product_info(seller_id: int, product_id: int):
    """Работает"""
    return utils.get_product_info(seller_id, product_id)

@app.post("/add_seller")
def add_seller(seller: SellerCreate):
    """Работает"""
    return utils.add_seller(seller.name, seller.avatar)

@app.post("/add_buyer")
def add_buyer(buyer: BuyerCreate):
    """Работает"""
    return utils.add_buyer(buyer.name)

@app.post("/add_product")
def add_product(product: ProductCreate):
    """Работает"""
    return utils.add_product(product.seller_id, product.picture)

@app.post("/add_product_info")
def add_product_info(product_info: ProductInfoCreate):
    return utils.add_product_info(product_info.seller_id, product_info.product_id, product_info.info)

@app.put("/update_seller_balance")
def update_seller_balance(update_balance: BalanceUpdate):
    """Работает"""
    return utils.update_seller_balance(update_balance.id, update_balance.pay)

@app.put("/update_user_balance")
def update_buyer_balance(update_balance: BalanceUpdate):
    """Работает"""
    return utils.update_buyer_balance(update_balance.id, update_balance.pay)
