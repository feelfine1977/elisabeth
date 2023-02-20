import csv
import sqlite3
from typing import Tuple


def delete_table(table_name):
    # Connect to the database
    conn = sqlite3.connect("p2p.db")
    cursor = conn.cursor()

    # Delete the table if it exists
    try:
        query = "DROP TABLE IF EXISTS {}".format(table_name)
        cursor.execute(query)
        print(f"Table {table_name} deleted.")
    except Exception as e:
        print(f"Error deleting table: {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    
def create_table_from_csv(file_path):
    # Connect to the database
    conn = sqlite3.connect("p2p.db")
    cursor = conn.cursor()

    # Get the name of the table based on the file name
    table_name = file_path.split(".")[0]

    # Create the table if it doesn't already exist
    try:
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            query = "CREATE TABLE IF NOT EXISTS {} ({})".format(table_name, ", ".join([f"{col} TEXT" for col in header]))
            cursor.execute(query)
    except Exception as e:
        print(f"Error creating table: {e}")
        return

    # Insert the data into the table
    try:
        with open(file_path, newline='') as f:
            reader = csv.reader(f)
            header = next(reader)
            query = "INSERT INTO {} ({}) VALUES ({})".format(
                table_name,
                ", ".join(header),
                ", ".join(["?" for _ in header])
            )
            for row in reader:
                try:
                    # Check if the data already exists in the table
                    case_id, event, timestamp = row[0], row[1], row[2]
                    check_query = f"SELECT * FROM {table_name} WHERE case_id = ? AND event = ? AND timestamp = ?"
                    cursor.execute(check_query, (case_id, event, timestamp))
                    if not cursor.fetchone():
                        # If the data doesn't exist, insert it
                        cursor.execute(query, row)
                except Exception as e:
                    print(f"Error inserting row {row}: {e}")
    except Exception as e:
        print(f"Error reading from file: {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
        
def read_data_from_table(table_name):
    connection = sqlite3.connect("p2p.db")
    cursor = connection.cursor()

    query = "SELECT * FROM {}".format(table_name)
    cursor.execute(query)

    data = cursor.fetchall()
    for row in data:
        print(row)

    connection.close()
    


def find_longest_process(table_name: str) -> Tuple[int, str, str, str, str, str, str, str]:
    conn = sqlite3.connect("p2p.db")
    cursor = conn.cursor()

    query = f"SELECT case_id, MIN(timestamp), MAX(timestamp) FROM {table_name} GROUP BY case_id ORDER BY MAX(timestamp) - MIN(timestamp) DESC LIMIT 1"
    cursor.execute(query)
    case_id, start, end = cursor.fetchone()

    query = f"SELECT * FROM {table_name} WHERE case_id = ? AND timestamp >= ? AND timestamp <= ?"
    cursor.execute(query, (case_id, start, end))
    result = cursor.fetchall()
    conn.close()

    return case_id, start, end, result










