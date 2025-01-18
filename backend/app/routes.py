from flask import Blueprint, render_template, request, jsonify
import base64
from openai import OpenAI

main = Blueprint('main', __name__)
client = OpenAI()

# Function to encode the image
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

@main.route('/', methods=['GET'])
def test():
    return jsonify({"status_code": "success", "message":"server is running!"}), 200

@main.route('/upload', methods=['POST'])
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
                        "text": "Is this a rock?",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )

    return jsonify(response.choices[0])