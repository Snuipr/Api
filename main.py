import psycopg2
from fastapi import FastAPI
from datetime import datetime

def get_buyer_from_id(id):
    """Работает"""
    conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buyers WHERE id = %s", (id,))
    result = cursor.fetchall()
    cursor.close()
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
    conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sellers WHERE id = %s", (id,))
    result = cursor.fetchall()
    cursor.close()
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
def get_product_from_id(id, product_id):
    """Работает"""
    conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE seller_id = %s and product_id = %s", (id, product_id))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(result) > 0:
        row = result[0]
        return ({
            "seller_id": row[0],
            "product_id": row[1],
            "picture": row[2]
        })
    return "Нет информации по этому ID"

def get_last_product_id(seller_id):
    conn = conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE seller_id = %s", (seller_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(result) > 0:
        row = result[-1]
        return ({"seller_id": row[0],
                 "product_id": row[1],
                 "picture": row[2]
        })
    return "Нет информации по этому ID"
def get_product_info_from_info(id, prod_id):
    """Работает"""
    conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM product_info WHERE seller_id = %s AND product_id = %s", (id, prod_id))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(result) > 0:
        row = result[0]
        return {
            "seller_id": row[0],
            "product_id": row[1],
            "info": row[2]
        }
    return "Нет информации по этому ID"

def get_check(id):
    """Работает"""
    conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM check WHERE id = %s", (id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if len(result) > 0:
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
    conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sellers(seller_name, avatar, data_register) VALUES (%s, %s, %s)", (name, avatar, date_time))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Ваш аккаунт успешно добавлен {date_time}"

def update_seller_balance(id, pay):
    """Работает"""
    info = get_seller_from_id(id)
    if type(info) == str:
        return info
    conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("UPDATE sellers SET balance = %s WHERE id = %s", (info["balance"] + pay, id))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Ваш баланс: {info['balance'] + pay}"

def add_new_user(name: str):
    conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO buyers(buyer_name) VALUES (%s)", (name,))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Ваш аккаунт успешно добавлен"

def update_user_balance(id, pay):
    info = get_buyer_from_id(id)
    if type(info) == str:
        return info
    conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    cursor.execute("UPDATE buyers SET balance = %s WHERE id = %s", (info["balance"] + pay, id))
    conn.commit()
    cursor.close()
    conn.close()
    return f"Ваш баланс: {info['balance'] + pay}"

def add_product_from_id(seller_id, picture):
    """Работает"""
    info = get_last_product_id(seller_id)
    conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    if type(info) == str:
        cursor.execute("INSERT INTO products(seller_id, product_id, picture) VALUES(%s, %s, %s)", (seller_id, 1, picture))
        conn.commit()
        cursor.close()
        conn.close()
        return "Ваш первый продукт"
    cursor.execute("INSERT INTO products(seller_id, product_id, picture) VALUES(%s, %s, %s)", (seller_id, info["product_id"]+1, picture))
    conn.commit()
    cursor.close()
    conn.close()
    return "Ваш не первый продукт"

def add_product_info_from_id(seller_id, product_id, text):
    inf1 = get_product_from_id(seller_id, product_id)
    if type(inf1) == str:
        return "Ошибка продукт не найден"
    info = get_product_info_from_info(seller_id, product_id)
    conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    cursor = conn.cursor()
    if type(info) == str:
        cursor.execute("INSERT INTO product_info(seller_id, product_id, info) VALUES(%s, %s, %s)", (seller_id, product_id, text))
        conn.commit()
        cursor.close()
        conn.close()
        return "Информация добавлена"
    cursor.execute("UPDATE product_info SET info = %s WHERE seller_id = %s AND product_id = %s", (text, seller_id, product_id))
    conn.commit()
    cursor.close()
    conn.close()
    return "Информация обновлена"

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
def get_product(id: int, product_id):
    """Работает"""
    return get_product_from_id(id, product_id)

@app.get("/product/info")
def get_product_info(id: int, product_id):
    """Работает"""
    return get_product_info_from_info(id, product_id)

@app.post("/add_seller")
def add_seller(name: str, avatar: str):
    """Работает"""
    return add_new_seller(name, avatar)

@app.post("/update_seller_balance")
def update_sel_balance(id: int, pay: int):
    """Работает"""
    return update_seller_balance(id, pay)

@app.post("/add_user")
def add_user(name: str):
    """Работает"""
    return add_new_user(name)

@app.post("/update_user_balance")
def add_us_balance(id: int, pay: int):
    """Работает"""
    return update_user_balance(id, pay)

@app.post("/add_product")
def add_product(seller_id: int, picture: str):
    """Работает"""
    return add_product_from_id(seller_id, picture)

@app.post("/add_product_info")
def add_product_info(seller_id: int, product_id: int, info: str):
    return add_product_info_from_id(seller_id, product_id, info)
