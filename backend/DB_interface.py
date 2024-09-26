from datetime import date
from typing import List
import mysql.connector
import json

def insert_data(data: List[dict]):
    insert_cmd = "INSERT INTO fruits_spoilage (item_name, Product_date, Expiry_date) VALUES (%s, %s, %s);"
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='Hack',
            user='root',
            password='Akash003!'
        )

        if connection.is_connected():
            print('Connected to MySQL database')

            # Create a cursor object using cursor() method
            cursor = connection.cursor()

            # SQL query to insert each record
            for record in data:
                insert_query = (record['Item_name'], record['Production_date'], record['Expiry_date'])
                cursor.execute(insert_cmd, insert_query)
            
            connection.commit()

    except mysql.connector.Error as error:
        print(f"Error inserting data: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

def Get_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='Hack',
            user='root',
            password='Akash003!'
        )

        if connection.is_connected():
            print('Connected to MySQL database')

            # Create a cursor object
            cursor = connection.cursor()

            # Query to get the latest record for each unique item_name
            read_query = """
                SELECT fs.item_name, fs.Product_date, fs.Expiry_date
                FROM fruits_spoilage fs
                INNER JOIN (
                    SELECT item_name, MAX(Product_date) AS latest_product_date
                    FROM fruits_spoilage
                    GROUP BY item_name
                ) latest_items 
                ON fs.item_name = latest_items.item_name 
                AND fs.Product_date = latest_items.latest_product_date;
            """
            cursor.execute(read_query)
            rows = cursor.fetchall()
            json_data = []

            # Iterate through rows and create JSON objects
            for row in rows:
                item_name, Product_date, Expiry_date = row

                # Convert date objects to strings
                if isinstance(Product_date, date):
                    Product_date = Product_date.isoformat()
                if isinstance(Expiry_date, date):
                    Expiry_date = Expiry_date.isoformat()

                data = {
                    'item_name': item_name,
                    'Product_date': Product_date,
                    'Expiry_date': Expiry_date,
                }
                json_data.append(data)

            # Return Python list as JSON
            return json_data

    except mysql.connector.Error as error:
        print(f"Error retrieving records: {error}")
        return {"error": str(error)}

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")