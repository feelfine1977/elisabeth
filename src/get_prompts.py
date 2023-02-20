import json
import sqlite3
import csv

def get_table_structure(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    return cursor.fetchall()

def build_json_prompts(db, table_name):
    conn = sqlite3.connect(db)
    table_structure = get_table_structure(conn, table_name)
    prompts = []
    id = 1

    # Build the prompt for finding the average case duration
    beginning = "Please generate a SQLLite query to "
    prompt_text = f"{beginning} find the average case duration for cases in the '{table_name}' table. The table has columns "
    for column in table_structure:
        prompt_text += f"'{column[1]}', "
    prompt_text = prompt_text[:-2] + "."
    prompts.append({"id": id, "prompt_text": prompt_text})
    id += 1

    # Build the prompt for finding the number of cases started in 2018
    prompt_text = f"{beginning} find the number of cases in the '{table_name}' table that were started in the year 2018. The table has columns "
    for column in table_structure:
        prompt_text += f"'{column[1]}', "
    prompt_text = prompt_text[:-2] + "."
    prompts.append({"id": id, "prompt_text": prompt_text})

    # Write the prompts to a JSON file
    with open("prompts.json", "w") as f:
        json.dump({"prompts": prompts}, f)
        


def build_json_prompts_from_file(file_questions,
                                 db, 
                                 table_name,file_output="prompts.json"):
    # Connect to the database
    conn = sqlite3.connect(db)
    table_structure = get_table_structure(conn, table_name)

    # Read the questions from the CSV file
    prompts = []
    id = 1
    with open(file_questions, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category = row["Category"]
            question = row["Question"]

            beginning = "Please generate a SQLLite query to "
            if category == "Event Log Data":
                prompt_text = f"{beginning} {question} from the '{table_name}' table. The table has columns "
                for column in table_structure:
                    prompt_text += f"'{column[1]}', "
                prompt_text = prompt_text[:-2] + "."
            elif category == "Analysis":
                prompt_text = f"{beginning} determine if the log adheres to the standard process. {question} The table has columns "
                for column in table_structure:
                    prompt_text += f"'{column[1]}', "
                prompt_text = prompt_text[:-2] + "."
            else:
                prompt_text = f"{beginning} {question}. The table has columns "
                for column in table_structure:
                    prompt_text += f"'{column[1]}', "
                prompt_text = prompt_text[:-2] + "."
            
            prompts.append({"id": id, "prompt_text": prompt_text})
            id += 1

    # Write the prompts to a JSON file
    with open(file_output, "w") as f:
        json.dump({"prompts": prompts}, f)
