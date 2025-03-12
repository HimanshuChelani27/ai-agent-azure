from flask import Flask, request, jsonify
import openai

# Flask app instance
app = Flask(__name__)

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = "YOUR_AZURE_AI_ENDPOINT"
AZURE_OPENAI_KEY = "YOUR_AZURE_AI_API_KEY"
DEPLOYMENT_NAME = "YOUR_AZURE_AI_API_DEPLOYMENT_NAME"

# Set up OpenAI client
client = openai.AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-01"
)

# Store chat history per user
chat_history = {}

def chat_with_ai(user_id, user_input):
    if user_id not in chat_history:
        chat_history[user_id] = [
            {"role": "system", "content": "You are a helpful AI assistant that remembers the conversation."}
        ]

    # Add user input to conversation history
    chat_history[user_id].append({"role": "user", "content": user_input})

    # Send conversation to Azure OpenAI
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=chat_history[user_id],
        temperature=0.7,
        max_tokens=200
    )

    # Extract AI response
    ai_response = response.choices[0].message.content

    # Add AI response to conversation history
    chat_history[user_id].append({"role": "assistant", "content": ai_response})

    return ai_response

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id", "default_user")  # Default user if not provided
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400

    ai_response = chat_with_ai(user_id, user_input)
    return jsonify({"user": user_input, "ai": ai_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
