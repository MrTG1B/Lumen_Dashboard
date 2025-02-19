from flask import Flask, request, jsonify
from flask_cors import CORS  # Enable CORS
from flask_socketio import SocketIO
import json

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

database_path = 'backend/database/database.json'

def load_database():
    with open(database_path) as f:
        return json.load(f)

def save_database(data):
    with open(database_path, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return "Lumen Dashboard Server is Running!", 200

@app.route('/<module_name>/ir/<state>', methods=['GET'])
def module_name_ir_state(module_name, state):
    data = load_database()
    if module_name in data:
        if state == 'on':
            return 'Turned on', 200
        elif state == 'off':
            return 'Turned off', 200
        return 'Invalid state', 400
    return 'Module not found', 404

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

@app.route('/<area_name>/<light_name>/<key>', methods=['GET'])
def area_name_light_name_key(area_name, light_name, key):
    data = load_database()
    try:
        return data[area_name]['lp'][light_name][key], 200
    except KeyError:
        return "Key/Light/Area not found", 404

@app.route('/<area_name>/<light_name>/lpdetails', methods=['GET'])
def area_name_light_name_lpdetails(area_name, light_name):
    data = load_database()
    return jsonify(data.get(area_name, {}).get('lp', {}).get(light_name, "Light not found")), 200

@app.route('/data', methods=['POST'])
def receive_data():
    content = request.json
    print(f"Received Data: {content}")
    return jsonify({"status": "success"}), 200

@app.route('/energy', methods=['POST'])
def receive_energy_data():
    content = request.json
    print(f"Received Energy Data: {content}")
    return jsonify({"status": "success"}), 200

@app.route('/fault', methods=['POST'])
def receive_fault_data():
    content = request.json
    print(f"Received Fault Data: {content}")
    return jsonify({"status": "success"}), 200

@socketio.on('/led/on')
def handle_led_on():
    print("LED ON command received via Socket.IO")

@socketio.on('/fault_search_result')
def handle_fault_search_result(data):
    print(f"Received fault search result from ESP32: {data}")
    
    # Forward the result to the client dashboard
    socketio.emit('/fault_search_response', data)
    
@socketio.on('/fault_search')
def handle_fault_search():
    print("Client requested fault search")
    
    # Emit fault search request to ESP32
    socketio.emit('/fault_search_esp')


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8080, debug=True)
