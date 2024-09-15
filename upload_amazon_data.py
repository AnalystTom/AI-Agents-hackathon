import pandas as pd
import mysql.connector
import sys

# Conversion rate from INR to USD
INR_TO_USD = 0.012

# Read the dataset
print("Reading dataset...")
df = pd.read_csv('Amazon-Products.csv', quotechar='"', skipinitialspace=True)

# Inspect the first few rows to ensure we have loaded the data correctly
print("Inspecting the first few rows of the dataset:")
print(df.head())

# Remove currency symbols and commas from 'discount_price' and 'actual_price', as well as 'no_of_ratings'
print("Cleaning data...")
df['discount_price'] = df['discount_price'].replace({'₹': '', ',': ''}, regex=True)
df['actual_price'] = df['actual_price'].replace({'₹': '', ',': ''}, regex=True)
df['no_of_ratings'] = df['no_of_ratings'].replace({',': ''}, regex=True)

# Convert columns to numeric, coercing errors to NaN for incorrect or missing values
df['discount_price'] = pd.to_numeric(df['discount_price'], errors='coerce')
df['actual_price'] = pd.to_numeric(df['actual_price'], errors='coerce')
df['ratings'] = pd.to_numeric(df['ratings'], errors='coerce')
df['no_of_ratings'] = pd.to_numeric(df['no_of_ratings'], errors='coerce')

# Convert prices from INR to USD
df['discount_price'] = df['discount_price'] * INR_TO_USD
df['actual_price'] = df['actual_price'] * INR_TO_USD

# Drop rows with NaN values
print("Dropping rows with NaN values...")
df.dropna(inplace=True)

# Print cleaned data to check the conversion
print("Cleaned data preview:")
print(df[['discount_price', 'actual_price', 'ratings', 'no_of_ratings']].head())
print(df.dtypes)

# sample 1000 rows
df = df.sample(1000)
print(f"Sampled data shape: {df.shape}")

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
    
    # Create the table if it does not exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS amazon_products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        main_category VARCHAR(255),
        sub_category VARCHAR(255),
        image TEXT,
        link TEXT,
        ratings FLOAT,
        no_of_ratings FLOAT,
        discount_price FLOAT,
        actual_price FLOAT
    );
    """
    cursor.execute(create_table_query)
    print("Table created successfully.")

    # check if any data in the table already, if yes then don't proceed
    cursor.execute("SELECT COUNT(*) FROM amazon_products")
    count = cursor.fetchone()[0]
    if count > 0:
        print(f"Table already contains {count} rows. Aborting insertion.")
        sys.exit(0)

    # Insert data into the table
    print("Inserting data into the table...")
    insert_query = """
    INSERT INTO amazon_products (name, main_category, sub_category, image, link, ratings, no_of_ratings, discount_price, actual_price)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    total_rows = df.shape[0]
    for i, (_, row) in enumerate(df.iterrows()):  # `i` is the iteration counter
        cursor.execute(insert_query, (
            row['name'],
            row['main_category'],
            row['sub_category'],
            row['image'],
            row['link'],
            row['ratings'],
            row['no_of_ratings'],
            row['discount_price'],
            row['actual_price']
        ))
        if i % 100 == 0:
            print(f"Progress: {i}/{total_rows} rows inserted ({i/total_rows*100:.2f}%)")


    conn.commit()
    print("Data inserted successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Database connection closed.")
