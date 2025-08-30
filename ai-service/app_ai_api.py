from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from waitress import serve

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure the Gemini API with your API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Get the URL of the chat history service from environment variables
CHAT_HISTORY_SERVICE_URL = os.environ.get('CHAT_HISTORY_SERVICE_URL')

@app.route('/healthz')
def health_check():
    return jsonify({"status": "healthy"}), 200




@app.route('/generate-response', methods=['POST'])
def generate_response():
    data = request.get_json()
    if not data or 'question' not in data or 'user_id' not in data:
        return jsonify({'error': 'No question or user ID provided'}), 400

    question = data['question']
    user_id = data['user_id']
    
    try:
        # Step 1: Save the user's message to the chat history service
        history_data = {
            'user_id': user_id,
            'role': 'user',
            'content': question
        }
        requests.post(f"{CHAT_HISTORY_SERVICE_URL}/history", json=history_data, timeout=5)

        # Step 2: Retrieve the entire chat history for the user
        history_response = requests.get(f"{CHAT_HISTORY_SERVICE_URL}/history/{user_id}", timeout=5)
        chat_history_list = history_response.json()
        
        # Step 3: Format the history for the Gemini API
        # The Gemini model expects roles 'user' and 'model'
        gemini_history = []
        for msg in chat_history_list:
            role = 'user' if msg['role'] == 'user' else 'model'
            gemini_history.append({'role': role, 'parts': [{'text': msg['content']}]})

        # Step 4: Start a new chat session with the full history
        chat_session = model.start_chat(history=gemini_history)
        
        # Step 5: Send the new question to the model
        gemini_response = chat_session.send_message(question)
        chat_response = gemini_response.text
        
        # Step 6: Save the AI's response to the chat history service
        ai_history_data = {
            'user_id': user_id,
            'role': 'assistant',
            'content': chat_response
        }
        requests.post(f"{CHAT_HISTORY_SERVICE_URL}/history", json=ai_history_data, timeout=5)

        return jsonify({'answer': chat_response})
        
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with chat history service: {e}")
        return jsonify({'error': f"Failed to connect to chat history service: {e}"}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': f"Sorry, an internal error occurred: {e}"}), 500

if __name__ == '__main__':
    # Use waitress for production deployment
    serve(app, host='0.0.0.0', port=5001)
