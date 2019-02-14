import json
import os

path = os.path.join(os.path.dirname(__file__),'parameters.json' )
with open(path) as f:
    data = json.load(f)
print(data["ABI"])
