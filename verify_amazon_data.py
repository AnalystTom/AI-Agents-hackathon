import mysql.connector

# Database connection details
config = {
    'user': 'Users',
    'password': 'AIagents2024Green',
    'host': '34.89.125.152',
    'port': '3306',
    'database': 'product-table',
}

conn = None
cursor = None

try:
    print("Connecting to the database...")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Query to select some rows from the table
    query = "SELECT * FROM amazon_products LIMIT 10"
    cursor.execute(query)

    # Fetch and print results
    results = cursor.fetchall()
    for row in results:
        print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")
except Exception as ex:
    print(f"Exception: {ex}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Database connection closed.")
