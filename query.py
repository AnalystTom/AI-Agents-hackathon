import mysql.connector

# Database connection details
config = {
    'user': '',  # Replace with your SQL username
    'password': '',  # Replace with your SQL password
    'host': '34.89.125.152',
    'port': '3306',# Replace with your SQL instance's public IP
    'database': 'product-table',  # Replace with your database name
}
conn = None
cursor=None
# Establish connection
try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Example query: Select all rows from the 'product_table'
    query = "SELECT Product_Name FROM product_table"
    cursor.execute(query)

    # Fetch and display results
    results = cursor.fetchall()
    for row in results:
        print(row)

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
