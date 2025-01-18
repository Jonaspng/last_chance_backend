from flask import Flask, request, jsonify
import base64
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Function to encode the image (for future use)
def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode("utf-8")

@app.route('/', methods=['GET'])
def test():
    return jsonify({"status_code": "success", "message": "Server is running!"}), 200

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    base64_image = encode_image(file)

    # Example OpenAI ChatGPT prompt
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that determines if images depict rocks."},
            {"role": "user", "content": "Is this a rock?"},
            # Note: Replace the line below with actual image processing if needed
            {"role": "user", "content": "Image data (base64): " + base64_image[:100] + "..."}
        ]
    )
    return jsonify({"status_code": "success", "message": response['choices'][0]['message']['content']}), 200

if __name__ == '__main__':
    app.run(debug=True)
