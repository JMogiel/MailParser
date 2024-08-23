import random
import time

from flask import Flask, request, jsonify

app = Flask(__name__)

# Store the order of processed phone numbers
processed_phone_numbers = []


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

    # Store the phone number after processing
    processed_phone_numbers.append(phone_number)

    # Check if this is the first processed phone number
    if len(processed_phone_numbers) == 1:
        print(f"Phone number {phone_number} was processed first")

    # Mock response to be returned
    response = {
        'status': 'success',
        'message': f'Received command {command} for phone number {phone_number}'
    }

    # Return the response as JSON
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(port=8000)
