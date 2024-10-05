from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import os
from langchain_ollama.llms import OllamaLLM

# Initialize Flask and allow CORS
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize LLM
ollama = OllamaLLM(base_url='http://localhost:11434', model='llama3.1')

# File to store conversations and memory
memory_file = 'bot_memory.json'
conversations_file = 'conversations.json'
chat_history_dir = 'Chat History'

# Load memory and conversations
def load_json(file_path, default_content):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:

        with open(file_path, 'w') as f:
            json.dump(default_content, f)
        return default_content
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default_content

memory = load_json(memory_file, {'facts': ["do not prompt \"I remember that conversation\" and any type of reminder of you memory unnecessary. Only do when it is really needed"], 'corrections': [], 'preferences': []})
conversations = load_json(conversations_file, [])

# Create directory for chat history
if not os.path.exists(chat_history_dir):
    os.makedirs(chat_history_dir)

# Custom instructions for the bot
def get_instructions():
    instructions = "You are developed by Lalit. Your are based on LLama3.1 8B model. You are a helpful chat assistant designed to provide accurate and information to the user. You remember past interactions. Here is what you know so far: \n"
    if memory['facts']:
        instructions += "Facts: " + ", ".join(memory['facts']) + ".\n"
    if memory['corrections']:
        instructions += "Corrections: " + ", ".join(memory['corrections']) + ".\n"
    return instructions + "Feel free to continue learning or discussing any topic."

# Save memory and conversations
def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to fetch all conversations
@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    convo_list = [{'id': convo['id'], 'title': convo['name']} for convo in conversations]
    return jsonify(convo_list)

# Endpoint to create a new conversation
@app.route('/api/conversations', methods=['POST'])
def create_conversation():
    new_id = len(conversations) + 1
    new_convo = {"id": new_id, "name": f"Conversation {new_id}", "messages": []}
    conversations.append(new_convo)
    save_json(conversations_file, conversations)
    return jsonify(new_convo), 201

# Endpoint to view a conversation (export to text file)
@app.route('/api/conversations/<int:convo_id>/export', methods=['GET'])
def export_conversation(convo_id):
    convo = next((c for c in conversations if c['id'] == convo_id), None)
    if not convo:
        return jsonify({"error": "Conversation not found."}), 404
    
    filename = f"Conversation_{convo_id}.txt"
    filepath = os.path.join(chat_history_dir, filename)
    
    with open(filepath, 'w') as f:
        for msg in convo['messages']:
            f.write(msg + "\n")
    
    return jsonify({"message": f"Conversation exported to {filepath}."})

# Endpoint to send and receive messages
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    convo_id = data.get('conversation_id')

    if not user_input or not convo_id:
        return jsonify({"error": "Invalid request."}), 400

    convo = next((c for c in conversations if c['id'] == convo_id), None)
    if not convo:
        return jsonify({"error": "Conversation not found."}), 404

    # Handle special commands
    if user_input.lower().startswith("learn:"):
        new_info = user_input[len("learn:"):].strip()
        memory['facts'].append(new_info)
        save_json(memory_file, memory)
        convo['messages'].append(f"You: {user_input}")
        convo['messages'].append("Bot: I've learned that!")
        save_json(conversations_file, conversations)
        return jsonify({"response": "I've learned that!"})

    if user_input.lower().startswith("correct:"):
        correct_info = user_input[len("correct:"):].strip()
        memory['corrections'].append(correct_info)
        save_json(memory_file, memory)
        convo['messages'].append(f"You: {user_input}")
        convo['messages'].append("Bot: Thanks for the correction! I'll remember that.")
        save_json(conversations_file, conversations)
        return jsonify({"response": "Thanks for the correction! I'll remember that."})

    if user_input.lower().startswith("forget:"):
        info_to_forget = user_input[len("forget:"):].strip()
        removed = False
        for category in memory:
            if info_to_forget in memory[category]:
                memory[category].remove(info_to_forget)
                removed = True
        if removed:
            save_json(memory_file, memory)
            convo['messages'].append(f"You: {user_input}")
            convo['messages'].append(f"Bot: I forgot {info_to_forget}.")
            save_json(conversations_file, conversations)
            return jsonify({"response": f"I forgot {info_to_forget}."})
        else:
            convo['messages'].append(f"You: {user_input}")
            convo['messages'].append("Bot: I couldn't find that information.")
            save_json(conversations_file, conversations)
            return jsonify({"response": "I couldn't find that information."})

    if user_input.lower() == 'recall':
        learned_info = "\n".join([f"{category.capitalize()}: {', '.join(data)}" for category, data in memory.items() if data])
        response = learned_info if learned_info else "I don't remember anything yet."
        convo['messages'].append(f"You: {user_input}")
        convo['messages'].append(f"Bot: {response}")
        save_json(conversations_file, conversations)
        return jsonify({"response": response})

    # Combine instructions and user input
    instructions = get_instructions()
    full_conversation = "\n".join([instructions] + convo['messages'] + [f"You: {user_input}"])

    # Get bot response
    bot_response = ollama.invoke(full_conversation)

    # Append messages to conversation
    convo['messages'].append(f"You: {user_input}")
    convo['messages'].append(f"Bot: {bot_response}")
    save_json(conversations_file, conversations)

    return jsonify({"response": bot_response})

# Endpoint to load a specific conversation's messages
@app.route('/api/conversations/<int:convo_id>/messages', methods=['GET'])
def get_conversation_messages(convo_id):
    convo = next((c for c in conversations if c['id'] == convo_id), None)
    if not convo:
        return jsonify({"error": "Conversation not found."}), 404
    return jsonify(convo['messages'])

# Start Flask server
if __name__ == '__main__':
    app.run(debug=True)
