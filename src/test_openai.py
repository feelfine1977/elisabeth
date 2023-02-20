import openai
import csv 
import yaml 

def get_api_key():
    # Load the secrets from the secrets.yaml file
    with open("/Users/urszulajessen/Documents/GitHub/elisabeth/src/secrets.yaml", "r") as file:
        secrets = yaml.load(file, Loader=yaml.FullLoader)
    return secrets["api_key"]

api_key = get_api_key()

def ask_openai(prompt, api_key):

    # Use the OpenAI API key to create a Codex client
    openai.api_key = api_key

    # Loop through each prompt in the JSON file
    queries = []

    response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            n=1,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=None
            )

    # Return the generated response
    result = response["choices"][0]["text"]
    queries.append([prompt, result])

# Add the prompt and result to a set
    prompt_result_set = set([tuple(query) for query in queries])


    # Open a csv file
    filename = 'openai_results.csv'
    fieldnames = ['prompt', 'result']
    with open(filename, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        for prompt_result in prompt_result_set:
            writer.writerow({'prompt': prompt_result[0], 'result': prompt_result[1]})

    return queries



#ask_openai("can you write the query for sqllite database to answer the question: :\n\n What is the average case duration?", api_key)
