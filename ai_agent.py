import openai

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT = "YOUR_AZURE_AI_ENDPOINT"
AZURE_OPENAI_KEY = "YOUR_AZURE_AI_API_KEY"
DEPLOYMENT_NAME = "YOUR_AZURE_AI_DEPLOYMENT_KEY"

# Set up OpenAI client
client = openai.AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_KEY,
    api_version="2024-02-01"  # Use the latest API version
)

# Initialize chat history
chat_history = [
    {"role": "system", "content": "You are a helpful AI assistant that remembers the conversation."}
]


def chat_with_ai(user_input):
    """
    Sends a user message to Azure OpenAI while maintaining conversation history.
    """
    global chat_history

    # Add user input to conversation history
    chat_history.append({"role": "user", "content": user_input})

    # Send the conversation to Azure OpenAI
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,  # Deployment name in Azure OpenAI
        messages=chat_history,
        temperature=0.7,
        max_tokens=200
    )

    # Extract AI response
    ai_response = response.choices[0].message.content

    # Add AI response to conversation history
    chat_history.append({"role": "assistant", "content": ai_response})

    return ai_response


# Continuous chat loop
if __name__ == "__main__":
    print("AI Chatbot (Type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("AI: Goodbye! Have a great day!")
            break

        response = chat_with_ai(user_input)
        print("AI:", response)
