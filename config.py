import json

'''
Load JSON data
'''
def load():
    with open('config.json', 'r') as f:
        data = json.load(f)
    return data