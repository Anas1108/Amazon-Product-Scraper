import os
import json

def save_to_json(data, filename):

    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
