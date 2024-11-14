import sqlite3
from tabulate import tabulate


def fetch_data_from_database():
    # Connect to the db.sqlite3 database file
    conn = sqlite3.connect("../db.sqlite3")

    # Create a cursor object
    cursor = conn.cursor()

    # Execute a query to fetch table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # Fetch the table names
    tables = cursor.fetchall()

    # Loop over the tables
    for table in tables:
        table_name = table[0]
        print(f"Table: {table_name}")

    # Execute a query to fetch data from the table
    cursor.execute(f"SELECT * FROM {table_name};")

    # Fetch the results
    results = cursor.fetchall()

    # Get the column names
    columns = [desc[0] for desc in cursor.description]

    # Format the results as a table
    table_data = tabulate(results, headers=columns, tablefmt="grid")

    # Display the table
    print(table_data)
    print()  # Print an empty line to separate tables

    # Close the cursor and the connection
    cursor.close()
    conn.close()


# Call the function to fetch table names
fetch_data_from_database()
