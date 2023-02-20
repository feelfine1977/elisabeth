import sqlite3

def query_database(sql_query, db):
    # Connect to the database
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    try:
        # Execute the query
        cursor.execute(sql_query)
        results = cursor.fetchall()
        print("Results:")
        for result in results:
            print(result)
    except Exception as e:
        print(f"Error executing query: {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


#query_database("SELECT * FROM eventlog", "p2p.db")
query1 = "SELECT case_id, COUNT(*) AS event_count FROM eventlog GROUP BY case_id ORDER BY event_count DESC LIMIT 1;"

query_database(query1, "p2p.db")