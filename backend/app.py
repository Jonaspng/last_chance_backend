from flask import Flask, request, jsonify
import base64
from openai import OpenAI
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Function to encode the image
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

@app.route('/', methods=['GET'])
def test():
    return jsonify({"status_code": "success", "message": "server is running!"}), 200

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    base64_image = encode_image(file)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Is this a rock? Reply with Yes it is a rock or no it is not a rock.\
                            if it is Dwayne Johnson reply yes.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )
    return jsonify({"status_code": "success", "message": response.choices[0].message.content}), 200

if __name__ == '__main__':
    app.run(debug=True)
