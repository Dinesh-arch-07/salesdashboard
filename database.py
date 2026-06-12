import pandas as pd
import mysql.connector

def load_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="DP77@dpdbs!@",
            database="sales_dashboard"
        )

        df = pd.read_sql("SELECT * FROM sales", conn)
        conn.close()
        return df

    except:
        return pd.read_csv("sales.csv")