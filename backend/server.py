from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import requests
import concurrent.futures
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)

database_path = 'backend/database/database.json'

# Ensure database file exists
if not os.path.exists(database_path):
    with open(database_path, 'w') as f:
        json.dump({}, f)

def load_database():
    with open(database_path) as f:
        return json.load(f)

def save_database(data):
    with open(database_path, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return "Lumen Dashboard Server is Running!", 200

@app.route('/arealist', methods=['GET'])
def arealist():
    data = load_database()
    return "\n".join(data.keys()), 200

@app.route('/area/<area_name>/lp', methods=['GET'])
def area_name_lp(area_name):
    data = load_database()
    if area_name in data:
        return "\n".join(data[area_name]['lp'].keys()), 200
    return "Area not found", 404

@app.route('/area/<area_name>/map', methods=['GET'])
def area_name_map(area_name):
    data = load_database()
    return data.get(area_name, {}).get('src', "Area not found"), 200

@app.route('/area/<area_name>/faulty_lp', methods=['GET'])
def area_name_faulty_lp(area_name):
    data = load_database()
    if area_name in data and data[area_name]['faulty_lp']:
        return "\n".join(data[area_name]['faulty_lp'].keys()), 200
    return "No faulty lights", 204

@app.route('/<path:area_name>/<path:light_name>/<path:key>', methods=['GET'])
def area_name_light_name_key(area_name, light_name, key):
    data = load_database()

    # Debugging logs
    # print(f"Received request for: {area_name}/{light_name}/{key}")

    # Decode URL parameters
    area_name = unquote(area_name)
    full_light_name = f"{light_name}/{key.split('/')[0]}"  # Rebuild the light name
    key = "/".join(key.split('/')[1:])  # Extract the actual key

    # print(f"Decoded values: Area: {area_name}, Light: {full_light_name}, Key: {key}")

    if area_name in data and "lp" in data[area_name]:
        if full_light_name in data[area_name]['lp'] and key in data[area_name]['lp'][full_light_name]:
            print(f"Returning: {data[area_name]['lp'][full_light_name][key]}")
            return data[area_name]['lp'][full_light_name][key], 200

    print("404 - Key/Light/Area not found")
    return "Key/Light/Area not found", 404


@app.route('/<path:area_name>/<path:light_name>/lpdetails', methods=['GET'])
def area_name_light_name_lpdetails(area_name, light_name):
    data = load_database()
    
    # Decode URL parameters
    area_name = unquote(area_name)
    light_name = unquote(light_name)

    return jsonify(data.get(area_name, {}).get('lp', {}).get(light_name, "Light not found")), 200

@app.route('/ir', methods=['POST'])
def receive_ir_state():
    content = request.json
    print(f"Received IR Data: {content}")
    
    data = load_database()
    lp_list = data["DG Block(Newtown)"]["lp"]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:  # Asynchronous execution
        for key, value in lp_list.items():
            if value["ip"] == content["deviceID"]:
                key_index = list(lp_list.keys()).index(key)
                
                if content["irState"] == 1:
                    futures = []
                    
                    if key_index != 0 and key_index != len(lp_list) - 1:
                        futures.append(executor.submit(requests.get, "http://" + lp_list[list(lp_list.keys())[key_index-1]]["ip"] + "/led/on"))
                        futures.append(executor.submit(requests.get, "http://" + lp_list[list(lp_list.keys())[key_index+1]]["ip"] + "/led/on"))
                    
                    elif key_index == 0:
                        futures.append(executor.submit(requests.get, "http://" + lp_list[list(lp_list.keys())[key_index+1]]["ip"] + "/led/on"))
                    
                    elif key_index == len(lp_list) - 1:
                        futures.append(executor.submit(requests.get, "http://" + lp_list[list(lp_list.keys())[key_index-1]]["ip"] + "/led/on"))

    return jsonify({"status": "success"}), 200

@app.route('/data', methods=['POST'])
def received_data():
    content = request.json
    print(f"Received Data: {content}")
    data=load_database()
    lp_list = data["DG Block(Newtown)"]["lp"]
    for key, value in lp_list.items():
        if value["ip"] == content["deviceID"]:
            data["DG Block(Newtown)"]["lp"][key]["current"]=content["current"]
            data["DG Block(Newtown)"]["lp"][key]["energy"]=content["energy"]
            # data["DG Block(Newtown)"]["lp"][key]["voltage"]=content["voltage"]
            # data["DG Block(Newtown)"]["lp"][key]["power"]=data["DG Block(Newtown)"]["lp"][key]["current"]*data["DG Block(Newtown)"]["lp"][key]["voltage"]
            break
        
        save_database(data)
    return jsonify({"status": "success"}), 200

@app.route('/fault', methods=['POST'])
def receive_fault_data():
    content = request.json
    print(f"Received Fault Data: {content}")
    return jsonify({"status": "success"}), 200

@app.route('/fault_search', methods=['POST'])
def fault_search():
    # content=request.json
    # area_name=content.get("area")
    data=load_database()
    lp_list = data["DG Block(Newtown)"]["lp"]
    # with concurrent.futures.ThreadPoolExecutor() as executor:  # Asynchronous execution
    for key, value in lp_list.items():
        # futures = []
        # futures.append(executor.submit(requests.get, "http://" + lp_list[key]["ip"] + "/fault_scan"))
        try:
            response=requests.get("http://" + lp_list[key]["ip"] + "/fault_scan")
            if response.status_code == 200:
                if response.text == "0":
                    data["DG Block(Newtown)"]["faulty_lp"][key]=lp_list[key]
                    data["DG Block(Newtown)"]["lp"][key]["faulty"] = True
                else:
                    data["DG Block(Newtown)"]["faulty_lp"].pop(key, None)
                    data["DG Block(Newtown)"]["lp"][key]["faulty"] = False
        except:
            pass
    save_database(data)
    # print(f"Received Fault Search: {content}")
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
