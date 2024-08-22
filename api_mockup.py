import random
import time

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/endpoint', methods=['POST'])
def receive_feedback():
    # Extract data from the request
    data = request.get_json()
    command = data.get('command')
    phone_number = data.get('phone_number')

    # Log received data (for debugging purposes)
    print(f"Received command: {command}, Received phone number: {phone_number}")

    # Random delay in response
    delay = random.randint(30, 120)
    print(f"Delaying response by {delay:.2f} seconds...")
    time.sleep(delay)

    # Mock response to be returned
    response = {
        'status': 'success',
        'message': f'Received command {command} for phone number {phone_number}'
    }

    # Return the response as JSON
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=8000)
