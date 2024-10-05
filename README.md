

```markdown
# Chatbot Project

## Description
This project is a conversational AI chatbot runtime built using Flask, LangChain, and Ollama. It is designed to engage in interactive conversations with users, learn from interactions, and store conversation history for future reference. The frontend is developed with HTML, CSS, and JavaScript, providing a user-friendly interface that allows users to easily interact with the chatbot. You can adjust the code and enjoy different models on ollama.

### Features
- Interactive chat interface with a responsive design
- Conversation history management
- Typing animation for bot responses
- Ability to view and save past conversations
- Learn from user interactions and correct mistakes
- Export Old chats in text format

## Getting Started

### Prerequisites
- Python 3.x
- Flask
- LangChain
- Ollama with ai model

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install the required Python packages:
   ```bash
   pip install Flask flask-cors langchain
   ```
3. Make sure the Ollama model is installed and running on your local machine.

### Running the Application
1. Start the Flask server:
   ```bash
   python chatbot.py
   ```
2. Open `index.html` in your browser to access the chatbot interface.

## Memory Commands
The chatbot has the following commands to manage memory and conversation history:

- **`/conversations`**: Lists all past conversations stored in memory.
- **`/view <id>`**: Views a specific conversation based on its ID. The conversation will be saved in a text file.
- **`/continue <id>`**: Continue a conversation based on its ID.

### Saving Conversations
- Conversations are automatically saved when a user interacts with the bot.
- The chatbot saves the conversation history in `memory.json` and can generate text files for specific conversations in the `Chat History` directory.

### File Structure
```
/Chatbot-Project
│
├── chatbot.py
├── bot_memory.json
├── index.html
├── styles.css
└── script.js
```

## Contributing
Feel free to fork the repository and submit pull requests for improvements and new features!

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Flask](https://flask.palletsprojects.com/)
- [LangChain](https://langchain.com/)
- [Ollama](https://ollama.com/)
```

### Instructions for Use:
- Replace `<repository-url>` and `<repository-directory>` with the actual URL and directory name of your project.
- You can add any additional sections as needed, like License, Acknowledgments, etc.

This README should provide a comprehensive overview of your chatbot project, its functionality, and how to get started with it!