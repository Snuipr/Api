import psycopg2

def create_db():
    print("Создание базы данных")
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="1", host="localhost", port="5432")
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute('CREATE DATABASE "API"')
        print("База данных создана")
    except psycopg2.errors.DuplicateDatabase:
        print("База данных 'API' уже существует.")
    finally:
        cursor.close()
        conn.close()

def create_table():
    conn = psycopg2.connect(dbname="API", user="postgres", password="1", host="localhost", port="5432")
    conn.autocommit = True
    cursor = conn.cursor()
    create_sellers_table = '''
        CREATE TABLE IF NOT EXISTS sellers (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            seller_name VARCHAR(50) UNIQUE NOT NULL,
            balance BIGINT DEFAULT 0,
            rating NUMERIC(2, 1) DEFAULT 0,
            num_sell BIGINT DEFAULT 0,
            avatar TEXT,
            data_register TIMESTAMP 
        )
        '''
    create_buyers_table = '''
        CREATE TABLE IF NOT EXISTS buyers (
        id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        buyer_name VARCHAR(50) UNIQUE NOT NULL,
        balance BIGINT DEFAULT 0,
        num_sell BIGINT DEFAULT 0   
        )
        '''
    create_products_table = '''
        CREATE TABLE IF NOT EXISTS products (
        seller_id BIGINT,
        product_id BIGINT,
        picture TEXT       
        )'''
    create_product_info_table = '''
        CREATE TABLE IF NOT EXISTS product_info (
        seller_id BIGINT,
        product_id BIGINT,
        info TEXT       
        )'''
    create_buy_check_table = '''
        CREATE TABLE IF NOT EXISTS buy_check (
        id BIGINT,
        buyer_balance BIGINT,
        data_buy TIMESTAMP
        )'''
    print("Создание таблицы продавцов")
    cursor.execute(create_sellers_table)
    print("Таблица продавцов создана")
    print("Создание таблицы покупателей")
    cursor.execute(create_buyers_table)
    print("Таблица покупателей создана")
    print("Создание таблицы продуктов")
    cursor.execute(create_products_table)
    print("Таблица продуктов создана")
    print("Создание таблицы информации о продукции")
    cursor.execute(create_product_info_table)
    print("Таблица информации о продукции создана")
    print("Создание таблицы с чеками")
    cursor.execute(create_buy_check_table)
    print("Таблица с чеками создана")
    cursor.close()
    conn.close()

create_db()
create_table()
