from flask import Flask
from flask_cors import CORS  # Ensure CORS is enabled
import os
import json
import urllib.parse

app = Flask(__name__)
port_number = 8080

# Enable CORS to allow cross-origin requests from the client
CORS(app)

@app.route('/arealist', methods=['GET'])
def arealist():
    with open('backend/database/database.json') as f:
        data = json.load(f)
        keys_str = "\n".join(data.keys())
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

@app.route('/<area_name>/<light_name>/<key>', methods=['GET'])
def area_name_light_name_key(area_name, light_name, key):
    try:
        # Decode URL-encoded light_name and area_name (optional, Flask does this automatically)
        decoded_area_name = urllib.parse.unquote(area_name)
        decoded_light_name = urllib.parse.unquote(light_name)
        decoded_key = urllib.parse.unquote(key)

        # Load the data from the JSON file
        with open('backend/database/database.json') as f:
            data = json.load(f)

            # Check if area_name exists in the data
            if decoded_area_name in data:
                # Check if light_name exists under the area's 'lp' key
                if decoded_light_name in data[decoded_area_name]['lp']:
                    # Check if the requested key exists for the light_name
                    if decoded_key in data[decoded_area_name]['lp'][decoded_light_name]:
                        return data[decoded_area_name]['lp'][decoded_light_name][decoded_key], 200
                    else:
                        print("Key not found")
                        return "Key not found", 404
                else:
                    print("Light not found")
                    return "Light not found", 404
            else:
                print("Area not found")
                return "Area not found", 404

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Server error", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port_number, debug=True)
