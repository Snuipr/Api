import psycopg2
from datetime import datetime

def get_buyer(id: int) -> dict:
    """Работает"""
    try:
        conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM buyers WHERE id = %s", (id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(result) > 0:
            row = result[0]
            return {
                "id": row[0],
                "name": row[1],
                "balance": row[2],
                "number_buy": row[3]
            }
    except Exception as error:
        raise error

def get_seller(id: int) -> dict:
    """Работает"""
    try:
        conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sellers WHERE id = %s", (id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(result) > 0:
            row = result[0]
            return {
                "id": row[0],
                "name": row[1],
                "balance": row[2],
                "rating": row[3],
                "number_sell": row[4],
                "avatar": row[5],
                "date_register": row[6]
            }
    except Exception as error:
        raise error

def get_product(seller_id: int, product_id: int) -> dict:
    """Работает"""
    try:
        conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE seller_id = %s and product_id = %s", (seller_id, product_id))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        if len(result) > 0:
            row = result[0]
            return {
                "seller_id": row[0],
                "product_id": row[1],
                "picture": row[2]
            }
    except Exception as error:
        raise error

def get_last_product_id(seller_id: int) -> int:
    """Работает"""
    try:
        conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE seller_id = %s", (seller_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        product_id = []
        if len(result) > 0:
            for row in result:
                product_id.append(row[1])
            return max(product_id)
    except Exception as error:
        raise error

def get_product_info(seller_id: int, product_id: int) -> dict:
    """Работает"""
    try:
        conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM product_info WHERE seller_id = %s AND product_id = %s", (seller_id, product_id))
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
    except Exception as error:
        raise error

def get_check(id: int) -> dict:
    """Работает"""
    try:
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
    except Exception as error:
        raise error

def add_seller(name: str, avatar: str) -> str:
    """Работает"""
    try:
        date_time = datetime.now().date()
        conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sellers(seller_name, avatar, data_register) VALUES (%s, %s, %s)", (name, avatar, date_time))
        conn.commit()
        cursor.close()
        conn.close()
        return f"Ваш аккаунт успешно добавлен {date_time}"
    except Exception as error:
        raise error

def add_buyer(name: str) -> None:
    """Работает"""
    try:
        conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO buyers(buyer_name) VALUES (%s)", (name,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as error:
        raise error

def add_product(seller_id: int, picture: str) -> None:
    """Работает"""
    try:
        info = get_last_product_id(seller_id)
        conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
        conn.autocommit = True
        cursor = conn.cursor()
        if not info:
            cursor.execute("INSERT INTO products(seller_id, picture) VALUES(%s, %s)", (seller_id, picture))
        else:
            cursor.execute("INSERT INTO products(seller_id, product_id, picture) VALUES(%s, %s, %s)", (seller_id, info + 1, picture))
        cursor.close()
        conn.close()
    except Exception as error:
        raise error

def add_product_info(seller_id: int, product_id: int, text: str) -> None:
    """Работает"""
    try:
        conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
        cursor = conn.cursor()
        conn.autocommit = True
        inf1 = get_product(seller_id, product_id)
        info = get_product_info(seller_id, product_id)
        if not inf1:
            return None
        if not info:
            cursor.execute("INSERT INTO product_info(seller_id, product_id, info) VALUES(%s, %s, %s)", (seller_id, product_id, text))
        else:
            cursor.execute("UPDATE product_info SET info = %s WHERE seller_id = %s AND product_id = %s", (text, seller_id, product_id))
        cursor.close()
        conn.close()
    except Exception as error:
        raise error

def update_seller_balance(id: int, pay: int) -> None:
    """Работает"""
    try:
        info = get_seller(id)
        if not info:
            return None
        conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute("UPDATE sellers SET balance = %s WHERE id = %s", (info["balance"] + pay, id))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as error:
        raise error

def update_buyer_balance(id: int, pay: int) -> None:
    """Работает"""
    try:
        info = get_buyer(id)
        if not info:
            return None
        conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
        cursor = conn.cursor()
        cursor.execute("UPDATE buyers SET balance = %s WHERE id = %s", (info["balance"] + pay, id))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as error:
        raise error

