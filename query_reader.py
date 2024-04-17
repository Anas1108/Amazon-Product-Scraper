import json

def read_queries():
    try:
        with open('user_queries.json') as f:
            product_names = json.load(f)
        return product_names
    except FileNotFoundError:
        print("Error: The file 'user_queries.json' was not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from 'user_queries.json'.")
        return []
