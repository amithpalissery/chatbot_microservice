from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure the Gemini API with your API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# This endpoint generates the AI response
@app.route('/generate-response', methods=['POST'])
def generate_response():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'No question provided'}), 400

    question = data['question']
    
    try:
        response = model.generate_content(question)
        chat_response = response.text
        return jsonify({'answer': chat_response})
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({'error': f"Sorry, an error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
