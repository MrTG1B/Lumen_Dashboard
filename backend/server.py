from flask import Flask
from flask_cors import CORS  # Ensure CORS is enabled
import os
import json

app = Flask(__name__)
port_number = 8080

# Enable CORS to allow cross-origin requests from the client
CORS(app)

@app.route('/arealist', methods=['GET'])
def arealist():
    with open('backend/database/database.json') as f:
        data = json.load(f)
        
        # Convert the keys to a string with each key on a new line
        keys_str = "\n".join(data.keys())
        
        # Print the formatted string
        print(keys_str)
        return keys_str, 200

@app.route('/area/<area_name>/lp', methods=['GET'])
def area_name_lp(area_name):
    with open('backend/database/database.json') as f:
        data = json.load(f)
        if area_name in data:
            lp_keys="\n".join(data[area_name]['lp'].keys())
            return lp_keys, 200
        else:
            return "Area not found", 404
        
@app.route('/area/<area_name>/map', methods=['GET'])
def area_name_src(area_name):
    with open('backend/database/database.json') as f:
        data = json.load(f)
        if area_name in data:
            return data[area_name]['src'], 200
        else:
            return "Area not found", 404

@app.route('/area/<area_name>/faulty_lp', methods=['GET'])
def area_name_faulty_lp(area_name):
    with open('backend/database/database.json') as f:
        data = json.load(f)
        if area_name in data:
            if data[area_name]['faulty_lp']:
                faulty_lp_keys="\n".join(data[area_name]['faulty_lp'].keys())
                return faulty_lp_keys, 200
            else:
                return "No faulty lights", 204
        else:
            return "Area not found", 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port_number, debug=True)
