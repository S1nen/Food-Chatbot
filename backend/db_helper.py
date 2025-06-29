import mysql.connector
from dns.e164 import query


# connection = mysql.connector.connect(
#     host     = "localhost",
#     user     = "root",
#     password = "(@j12^12",
#     database = "pandeyji_eatery"

# )


from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()


MYSQLHOST = os.getenv("MYSQLHOST")
MYSQLUSER = os.getenv("MYSQLUSER")
MYSQLPASSWORD = os.getenv("MYSQLPASSWORD")
MYSQLDATABASE = os.getenv("MYSQLDATABASE")
MYSQLPORT = int(os.getenv("MYSQLPORT", 3306))
CA_PATH = Path(__file__).resolve().parent / "certs" / "ca.pem"



connection = mysql.connector.connect(
    host=MYSQLHOST,
    user=MYSQLUSER,
    password=MYSQLPASSWORD,
    database=MYSQLDATABASE,
    port=MYSQLPORT,
    ssl_ca=str(CA_PATH)
)

print("✅ Connected to Aiven MySQL")

def insert_order_item(food_items,quantity,order_id):
    try:
        cursor=connection.cursor()
        cursor.callproc("insert_order_item",(food_items,quantity,order_id))
        connection.commit()
        cursor.close()
        print("Order item inserted successfully!")
        return 1

    except mysql.connector.Error as err:
        print(f"Error inserting order item:{err}")
        connection.rollback()
        return -1

    except Exception as e:
        print(f"An error occurred:{e}")
        connection.rollback()
        return -1


def get_next_order_id():
    cursor=connection.cursor()

    query="SELECT MAX(order_id) FROM orders"
    cursor.execute(query)
    row=cursor.fetchone()
    cursor.close()

    result = row[0] if row[0] is not None else 0
    return result + 1




def get_total_price(order_id):
    cursor=connection.cursor()
    query=f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    result=cursor.fetchone()[0]
    cursor.close()
    return result

def insert_order_tracking_state(order_id,status):
    cursor=connection.cursor()

    query="INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(query,(order_id, status))

    connection.commit()
    cursor.close()


def get_order_status(order_id: int):

    cursor = connection.cursor()
    query = "SELECT status FROM order_tracking WHERE order_id = %s"
    cursor.execute(query, (order_id,))
    result = cursor.fetchone()

    cursor.close()

    return result[0] if result else None


def get_id_from_db(order_id:int):
    cursor=connection.cursor()
    query="SELECT order_id FROM orders WHERE order_id=%s"
    cursor.execute(query,(order_id,))
    id=cursor.fetchall()
    cursor.close()

    return id

def delete_from_db(order_id:int):
    cursor=connection.cursor()
    cursor.execute("START transaction;")
    cursor.execute("UPDATE order_tracking SET order_tracking.status='cancelled' WHERE order_id=%s",(order_id,))
    cursor.execute("DELETE FROM orders WHERE order_id=%s",(order_id,))
    connection.commit()
    cursor.close()


