import json
import os 


def extract_json(path: str, needed_keys = None) :
    with open(path, 'r', encoding ='utf-8') as f:
        data = json.load(f)

    if needed_keys is None:
        return data 

    if isinstance(data, list):
        return [
            {key: item.get(key) for key in needed_keys}
            for item in data
        ]
    if isinstance(data, dict):
        return {key: data.get(key) for key in needed_keys}
    
    raise ValueError("Unexpected JSON format")
    
