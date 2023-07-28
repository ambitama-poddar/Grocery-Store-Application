from sql_connection import get_sql_connection

def get_all_products(connection):
    query = "SELECT products.product_id, products.name, products.uom_id, products.price_per_unit, uom.uom_name FROM grocery_store.products INNER JOIN grocery_store.uom ON products.uom_id = uom.uom_id"

    with connection.cursor() as cursor:
        cursor.execute(query)
        response = [
            {
                "product_id": product_id,
                "name": name,
                "uom_id": uom_id,
                "price_per_unit": price_per_unit,
                "uom_name": uom_name
            }
            for (product_id, name, uom_id, price_per_unit, uom_name) in cursor
        ]

    return response

def insert_new_product(connection, product):
    query = "INSERT INTO products (name, uom_id, price_per_unit) VALUES (%s, %s, %s)"

    with connection.cursor() as cursor:
        cursor.execute(query, (product['product_name'], product['uom_id'], product['price_per_unit']))
        connection.commit()
        return cursor.lastrowid

def delete_product(connection, product_id):
    query = "DELETE FROM products WHERE product_id = %s"

    with connection.cursor() as cursor:
        cursor.execute(query, (product_id,))
        connection.commit()
        return product_id

if __name__ == "__main__":
    connection = get_sql_connection()

    # Uncomment the following lines to test the functions
    
    # product = {
    #     "product_name": "Mango",
    #     "uom_id": 1,
    #     "price_per_unit": 100
    # }

    # print(delete_product(connection, 17))
    # print(delete_product(connection, 19))
    # insert_new_product(connection, product)
