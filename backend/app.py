
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Ollama configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")

# Cooking system prompt
COOKING_SYSTEM_PROMPT = """You are a helpful cooking assistant and recipe provider. You specialize in:
- Providing detailed cooking recipes with ingredients and step-by-step instructions
- Answering cooking techniques and tips questions
- Suggesting recipe modifications for dietary restrictions
- Helping with meal planning and ingredient substitutions
- Explaining cooking terminology and methods

Always provide clear, practical advice. When providing recipes:
1. List all ingredients with measurements
2. Provide step-by-step instructions
3. Include cooking times and temperatures
4. Add helpful tips or variations
5. Mention difficulty level and serving size

Be friendly, encouraging, and make cooking accessible for all skill levels."""

# Store conversation history (in production, use a database)
conversation_history = []

class CookingChatbot:
    def __init__(self):
        self.base_url = OLLAMA_BASE_URL
        self.model = OLLAMA_MODEL

    def generate_response(self, messages):
        """Generate response using Ollama's chat API"""
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "num_predict": 500  # Use num_predict for max tokens in Ollama
                    }
                },
                timeout=120
            )

            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            result = response.json()
            # The response from /api/chat is nested under the 'message' key
            return result.get("message", {}).get("content", "Sorry, I couldn't generate a response.")

        except requests.exceptions.HTTPError as e:
            # Provide more specific feedback for HTTP errors
            error_details = e.response.text
            return f"HTTP Error: {e.response.status_code} - {error_details}"
        except requests.exceptions.RequestException as e:
            return f"Connection error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

# Initialize the chatbot
chatbot = CookingChatbot()

@app.route('/')
def home():
    return jsonify({
        "message": "Cooking Recipe Chatbot API is running!",
        "endpoints": {
            "/chat": "POST - Send a message to the chatbot",
            "/health": "GET - Check API health",
            "/reset": "POST - Reset conversation history"
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test connection to Ollama
        response = requests.get(f"{OLLAMA_BASE_URL}/api/version", timeout=5)
        ollama_status = "connected" if response.status_code == 200 else "disconnected"
    except:
        ollama_status = "disconnected"

    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "ollama_status": ollama_status,
        "model": OLLAMA_MODEL
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400

        user_message = data['message'].strip()

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Construct the message history for the /api/chat endpoint
        messages = [{"role": "system", "content": COOKING_SYSTEM_PROMPT}]

        # Add past conversation (last 5 exchanges)
        for item in conversation_history[-5:]:
            messages.append({"role": "user", "content": item['user']})
            messages.append({"role": "assistant", "content": item['bot']})

        # Add the new user message
        messages.append({"role": "user", "content": user_message})

        # Generate response
        bot_response = chatbot.generate_response(messages)

        # TODO: Add error checking for bot_response here before appending
        # Store in conversation history
        conversation_history.append({
            "user": user_message,
            "bot": bot_response,
            "timestamp": datetime.now().isoformat()
        })

        return jsonify({
            "user_message": user_message,
            "bot_response": bot_response,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({"message": "Conversation history reset successfully"})

if __name__ == '__main__':
    print("Starting Cooking Recipe Chatbot API...")
    print(f"Attempting to connect to Ollama at: {OLLAMA_BASE_URL}")
    print(f"Using model: {OLLAMA_MODEL}")
    print("Run 'ollama list' in your terminal to ensure the model is available.")
    print("API will be accessible at: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
