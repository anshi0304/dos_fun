import logging
from flask import Flask, jsonify, request
import time
import psutil  # To monitor CPU and memory usage

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/')
def home():
    start_time = time.time()  # Track response time

    # Example processing (could add heavier computations here)
    response = jsonify({"message": "Welcome to the server!"})
    
    # Calculate response time
    response_time = time.time() - start_time

    # Log diagnostics
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    logging.info(f"Response Time: {response_time:.4f}s | CPU Usage: {cpu_usage}% | Memory Usage: {memory_usage}%")
    
    return response

@app.route('/status')
def status():
    """Endpoint to check server status."""
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    return jsonify({
        "status": "Server is running",
        "cpu_usage": f"{cpu_usage}%",
        "memory_usage": f"{memory_usage}%"
    })

@app.route('/heavy')
def heavy():
    start_time = time.time()  # Track start time
    
    # Simulate heavy computation
    result = sum(i * i for i in range(10**6))
    
    # Get client IP address
    client_ip = request.remote_addr

    # Calculate diagnostics
    response_time = time.time() - start_time
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    
    # Log diagnostics with client IP
    app.logger.info(
        f"/heavy - Response Time: {response_time:.4f}s | CPU Usage: {cpu_usage}% | Memory Usage: {memory_usage}% | Client IP: {client_ip}"
    )
    
    # Return diagnostics, computation result, and client IP
    return jsonify({
        "message": f"Heavy computation done for client at {client_ip}",
        "client_ip": client_ip,
        "result": result,
        "response_time": f"{response_time:.4f} seconds",
        "cpu_usage": f"{cpu_usage}%",
        "memory_usage": f"{memory_usage}%"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
