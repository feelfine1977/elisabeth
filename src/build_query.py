import json
import openai
import sqlite3

import pandas as pd

def ask_openai(filename, api_key):
    # Load the prompts from the JSON file
    with open(filename, "r") as f:
        prompts = json.load(f)["prompts"]

        # Use the OpenAI API key to create a Codex client
        openai.api_key = api_key

        # Loop through each prompt in the JSON file
        queries = []
        for prompt in prompts:
            question = prompt["prompt_text"]
            
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=question,
                temperature=0.5,
                n=1,
                max_tokens=1024,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=None
                )

            # Return the generated response
            message = response["choices"][0]["text"]
            queries.append(message)

    return queries



def query_database(prompts_file, api_key):
    # Ask Codex to create a query for the given question
    queries = ask_openai(prompts_file, api_key)

    # Connect to the database
    conn = sqlite3.connect("p2p.db")
    cursor = conn.cursor()
    results = []
    for prompt_id, prompt in enumerate(queries):
        # Execute the query
        try:
            cursor.execute(prompt)
            query_results = cursor.fetchall()
            for result in query_results:
                results.append([prompt_id, prompt, result])
        except Exception as e:
            print(f"Error executing query: {e}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Create a dataframe from the results
    df = pd.DataFrame(results, columns=["id", "query", "result"])
    df.to_csv("queries_results.csv", index=False)
    return df
