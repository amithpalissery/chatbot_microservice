from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# This route serves the HTML file for the user interface
@app.route('/')
def home():
    return render_template('question.html', chat_history=[])

# This route forwards the user's question to the AI microservice
@app.route('/chatbot', methods=['POST'])
def chatbot():
    question = request.form.get('question')
    if not question:
        return jsonify({'answer': 'Please enter a question.'}), 400

    try:
        # NOTE: Replace 'http://127.0.0.1:5001' with your AI microservice's IP and port.
        ai_api_url = "http://ai-service:5001/generate-response"
        
        # Send the user's question to the AI service as JSON
        response = requests.post(ai_api_url, json={'question': question})
        response.raise_for_status()
        
        # The AI microservice returns a JSON response
        ai_response_data = response.json()
        ai_response_text = ai_response_data.get('answer', 'An unexpected error occurred.')

        return jsonify({'answer': ai_response_text})

    except requests.exceptions.RequestException as e:
        print("Error connecting to AI microservice:", e)
        return jsonify({'answer': f"Sorry, an error occurred while connecting to the AI service: {e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
