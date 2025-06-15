"""
import mysql.connector

connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password="(@j12^12",
    database="pandeyji_eatery"
)

def get_order_status(order_id:int):
    cursor=connection.cursor()
    query=("SELECT status FROM order_tracking WHERE order_id=%s")
    cursor.execute(query,(order_id,))
    result=cursor.fetchone()

    cursor.close()
    connection.close()

    if result is not None:
        return result[0]
    else:
        return None

"""

# db_helper.py
import mysql.connector

def get_order_status(order_id: int):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="(@j12^12",
        database="pandeyji_eatery"
    )

    cursor = connection.cursor()
    query = "SELECT status FROM order_tracking WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result[0] if result else None
