from datetime import datetime
from sql_connection import get_sql_connection
import mysql.connector

def insert_order(connection, order):
    try:
        with connection.cursor() as cursor:
            order_query = ("INSERT INTO orders "
                           "(customer_name, total, datetime) "
                           "VALUES (%s, %s, %s)")
            order_data = (order['customer_name'], order['grand_total'], datetime.now())

            cursor.execute(order_query, order_data)

            order_id = cursor.lastrowid

            order_details_query = ("INSERT INTO order_details "
                                   "(order_id, product_id, quantity, total_price) "
                                   "VALUES (%s, %s, %s, %s)")

            order_details_data = []
            for order_detail_record in order['order_details']:
                order_details_data.append((
                    order_id,
                    int(order_detail_record['product_id']),
                    float(order_detail_record['quantity']),
                    float(order_detail_record['total_price'])
                ))

            cursor.executemany(order_details_query, order_details_data)
            connection.commit()

            return order_id

    except mysql.connector.Error as err:
        connection.rollback()
        if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
            print("Error: Duplicate entry. Please check your data.")
        else:
            print(f"Error occurred: {err}")
        return None

if __name__ == '__main__':
    connection = get_sql_connection()
    order_data = {
        'customer_name': 'Mohan',
        'grand_total': 90,
        'order_details': [
            {
                'product_id': 4,
                'quantity': 2,
                'total_price': 40
            }
        ]
    }
    order_id = insert_order(connection, order_data)
    if order_id is not None:
        print(f"Order successfully inserted with ID: {order_id}")
    else:
        print("Failed to insert the order.")