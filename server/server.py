from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# Simulated completion time
completion_time = 5  # seconds
start_time = time.time()

@app.route('/status', methods=['GET'])
def get_status():
    current_time = time.time()
    elapsed_time = current_time - start_time
    
    if elapsed_time < completion_time:
        return jsonify({"result": "pending"})
    
    # Simulate random error or success
    if random.random() < 0.1:
        return jsonify({"result": "error"})
    return jsonify({"result": "completed"})

if __name__ == '__main__':
    app.run(debug=True)
