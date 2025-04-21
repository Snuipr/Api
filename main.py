import psycopg2
from fastapi import FastAPI
from datetime import datetime

def get_buyer_from_id(id):
    """Работает"""
    conn = psycopg2.connect(dbname="krestiki_noliki", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buyers WHERE id = %s", id)
    result = cursor.fetchall()
    conn.close()
    if len(result) > 0:
        row = result[0]
        return ({
            "id": row[0],
            "name": row[1],
            "balance": row[2],
            "number_buy": row[3]
        })
    return "Нет информации по ID"

def get_seller_from_id(id):
    """Работает"""
    conn = psycopg2.connect(dbname="krestiki_noliki", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sellers WHERE id = %s", (id, ))
    result = cursor.fetchall()
    conn.close()
    if len(result) > 0:
        row = result[0]
        return ({
            "id": row[0],
            "name": row[1],
            "balance": row[2],
            "rating": row[3],
            "number_sell": row[4],
            "avatar": row[5],
            "date_register": row[6]
        })
    return "Нет информации по этому ID"
def get_product_from_id(id):
    """Работает"""
    conn = psycopg2.connect(dbname="krestiki_noliki", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = %s", id)
    result = cursor.fetchall()
    conn.close()
    if len(result) > 0:
        row = result
        return ({
            "id": row[0],
            "picture": row[1]
        })
    return "Нет информации по этому ID"
def get_product_info_from_info(id):
    """Работает"""
    conn = psycopg2.connect(dbname="krestiki_noliki", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products_info WHERE id = %s", id)
    result = cursor.fetchone()
    conn.close()
    if result > 0:
        row = result[0]
        return {
            "id": row[0],
            "info": row[1]
        }
    return "Нет информации по этому ID"

def get_check(id):
    """Работает"""
    conn = psycopg2.connect(dbname="krestiki_noliki", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM check WHERE id = %s", id)
    result = cursor.fetchone()
    conn.close()
    if result > 0:
        row = result[0]
        return {
            "id": row[0],
            "user_balance": row[1],
            "data_buy": row[2]
        }
    return "Нет информации по этому ID"

def add_new_seller(name: str, avatar: str):
    """Работает"""
    date_time = datetime.now().date()
    conn = psycopg2.connect(dbname="krestiki_noliki", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sellers(name, balance, avatar, data_register) VALUES (%s, %s, %s, %s)", (name, avatar, date_time))
    conn.commit()
    conn.close()
    return f"Ваш аккаунт успешно добавлен {datetime}"

def add_seller_balance(id, balance):
    """Работает"""
    info = get_seller_from_id(id)
    conn = psycopg2.connect(dbname="krestiki_noliki", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("UPDATE sellers SET balance = %s WHERE id = %s", (info["balance"] + balance, id,))
    conn.commit()
    conn.close()
    return f"Ваш баланс: {info['balance'] + balance}"

app = FastAPI()


@app.get("/seller/info")
def get_seller(id: int):
    """Работает"""
    return get_seller_from_id(id)

@app.get("/seller/list")
def get_seller_from_pagination(offset: int = 0, fetch: int = 5):
    """Работает"""
    seller_list = []
    for id in range(offset, fetch+1):
        seller_list.append(get_seller_from_id(id))
    return seller_list

@app.get("/user")
def get_user_from_id(id: int):
    """Работает"""
    return get_buyer_from_id(id)

@app.get("/product")
def get_product(id: int):
    """Работает"""
    return get_product_from_id(id)

@app.get("/product/info")
def get_product_info(id: int):
    """Работает"""
    return get_product_info_from_info(id)

@app.post("/add_seller")
def add_seller(name: str, avatar: str):
    """Работает"""
    return add_new_seller(name, avatar)

@app.post("/add_balance")
def add_balance(id: int, pay: int):
    """Работает"""
    return add_seller_balance(id, pay)
