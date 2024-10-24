from flask import Flask, jsonify, request
import random
import time

app = Flask(__name__)

# Simulated completion time
completion_time = 10  # seconds
start_time = time.time()

@app.route('/status', methods=['GET'])
def get_status():
    global start_time

    current_time = time.time()
    elapsed_time = current_time - start_time
    
    if elapsed_time < completion_time:
        return jsonify({"result": "pending"})
    
    # Simulate random error or success
    if random.random() < 0.1:
        return jsonify({"result": "error"})
    return jsonify({"result": "completed"})

@app.route('/set_completion_time', methods=['POST'])
def set_completion_time():
    global completion_time, start_time
    
    # Get the completion time from the client request
    data = request.get_json()
    completion_time = data.get('completion_time', 10)
    start_time = time.time()  # Reset start time when new completion time is set
    return jsonify({"message": "Completion time set", "completion_time": completion_time})

if __name__ == '__main__':
    app.run(debug=True)
