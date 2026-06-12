import mysql.connector
import pandas as pd

def load_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DP77@dpdbs!@",
        database="sales_dashboard"
    )

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sales")

    rows = cursor.fetchall()

    # FORCE CLEAN COLUMN NAMES
    columns = [i[0].strip() for i in cursor.description]

    df = pd.DataFrame(rows, columns=columns)

    conn.close()
    return df