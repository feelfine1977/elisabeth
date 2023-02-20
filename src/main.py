import yaml
from add_data import create_table_from_csv
from get_prompts import  build_json_prompts_from_file
from build_query import query_database

def get_api_key():
    # Load the secrets from the secrets.yaml file
    with open("/Users/urszulajessen/Documents/GitHub/elisabeth/src/secrets.yaml", "r") as file:
        secrets = yaml.load(file, Loader=yaml.FullLoader)
    return secrets["api_key"]

#add data if not added

api_key = get_api_key()

create_table_from_csv('eventlog.csv')

# Create the prompts.json file
#prompt_data = build_json_prompts("p2p.db", "eventlog")
build_json_prompts_from_file("pmquestions_short.csv","p2p.db", "eventlog", "prompts_1.json")
df = query_database("prompts_1.json", api_key)
print(df)

#question = "can you write the query for sqllite database to answer the question: :\n\n"
#question += " What is the average case duration?"
#query_database(question, api_key)


