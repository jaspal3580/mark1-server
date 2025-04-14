from flask import Flask, request, jsonify
import json
import uuid
import os

app = Flask(__name__)

DATA_FILE = 'devices.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def home():
    return 'Welcome to GURLEEN Cloud Server!'

@app.route('/register', methods=['GET'])
def register():
    data = load_data()
    token = str(uuid.uuid4())
    data[token] = {f"V{i}": "" for i in range(100)}
    save_data(data)
    return jsonify({"auth_token": token})

@app.route('/update/<token>/<pin>/<value>', methods=['GET'])
def update_pin(token, pin, value):
    data = load_data()
    if token in data and pin in data[token]:
        data[token][pin] = value
        save_data(data)
        return jsonify({"status": "success", "message": f"{pin} set to {value}"})
    return jsonify({"status": "error", "message": "Invalid token or pin"})

@app.route('/get/<token>/<pin>', methods=['GET'])
def get_pin(token, pin):
    data = load_data()
    if token in data and pin in data[token]:
        return jsonify({"value": data[token][pin]})
    return jsonify({"status": "error", "message": "Invalid token or pin"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)