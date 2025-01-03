import mysql.connector

from datetime import date, datetime
from typing import Union, List, Dict

# To get fruit names and ids
def get_fruit_records():
    # Create the connection to the MySQL database
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
            cursor = connection.cursor(dictionary=True)

            # SQL query to fetch fruits where Expiry_date is NULL
            query = "SELECT item_name, item_id FROM fruits_spoilage;"
            cursor.execute(query)
            result = cursor.fetchall()

            return result

    except mysql.connector.Error as error:
        print(f"Error fetching data: {error}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

# To update the expiry date for the fruits
def update_expiry_date(fruit_id, expiry_date):
    # Create the connection to the MySQL database
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

            # SQL query to update the expiry date for a specific fruit
            update_query = "UPDATE fruits_spoilage SET Expiry_date = %s WHERE item_id = %s;"
            cursor.execute(update_query, (expiry_date, fruit_id))

            # Commit the changes
            connection.commit()

    except mysql.connector.Error as error:
        print(f"Error updating data: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

# To insert initial data from user
def insert_data(data: Union[List[Dict], Dict]):
    insert_cmd = "INSERT INTO fruits_spoilage (item_name, Product_date, Quantity) VALUES (%s, %s, %s);"
    
    try:
        # Connect to MySQL
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

            # Ensure the data is in list form, even if it's a single record
            if isinstance(data, dict):
                data = [data]

            # Log the received data for debugging purposes
            print("Data received for insertion:", data)

            # Get the current date (YYYY-MM-DD)
            current_date = datetime.now().strftime('%Y-%m-%d')

            # Insert each record
            for record in data:
                # Check if record is a dictionary and has the required keys
                if isinstance(record, dict) and 'name' in record and 'quantity' in record:
                    insert_query = (record['name'], current_date, record['quantity'])
                    cursor.execute(insert_cmd, insert_query)
                else:
                    print(f"Invalid record format: {record}")
            
            # Commit the changes to the database
            connection.commit()

    except mysql.connector.Error as error:
        print(f"Error inserting data: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

# To send data to frontend
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
                SELECT item_name, Product_date, Expiry_date, Quantity
                FROM fruits_spoilage;
            """
            cursor.execute(read_query)
            rows = cursor.fetchall()
            json_data = []

            # Iterate through rows and create JSON objects
            for row in rows:
                item_name, Product_date, Expiry_date, Quantity = row

                # Convert date objects to strings
                if isinstance(Product_date, date):
                    Product_date = Product_date.isoformat()
                if isinstance(Expiry_date, date):
                    Expiry_date = Expiry_date.isoformat()

                data = {
                    'item_name': item_name,
                    'Product_date': Product_date,
                    'Expiry_date': Expiry_date,
                    "Quantity": Quantity
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
