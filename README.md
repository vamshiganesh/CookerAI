# 🍳 Cooking Recipe Chatbot

A simple, self-hosted chatbot designed to be your personal cooking assistant. Get recipe ideas, detailed instructions, ingredient substitutions, and cooking tips right from your browser.

This project uses a Python Flask backend, a plain HTML/CSS/JS frontend, and is powered by a locally running Ollama instance with the Gemma model.

 <!-- It's a good idea to add a screenshot of your app here! -->

## ✨ Features

- **Conversational Interface**: Chat naturally to get the help you need.
- **Recipe Generation**: Ask for recipes based on ingredients, cuisine, or meal type.
- **Cooking Assistance**: Get help with ingredient substitutions, cooking techniques, and tips.
- **Local First**: Runs entirely on your local machine. No external API keys or internet connection required (after initial setup).
- **Conversation History**: The bot remembers the last few turns of your conversation for better context.
- **Simple & Extendable**: Built with a minimal technology stack that is easy to understand and modify.

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript (no frameworks)
- **AI Model**: Google Gemma (via Ollama)
- **CORS Handling**: Flask-Cors

## 🚀 Getting Started

Follow these steps to get the chatbot running on your local machine.

### Prerequisites

1.  **Python 3.8+**: Make sure you have Python installed. You can check with `python --version`.
2.  **Ollama**: You must have Ollama installed and running. Download it from ollama.com.

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd cooking-chatbot
```

### 2. Set Up the Backend

First, create and activate a virtual environment to manage dependencies.

```bash
# Navigate to the project root
# Create the virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (macOS/Linux)
# source venv/bin/activate
```

Next, install the required Python packages. A `requirements.txt` file is recommended for this.

```bash
# Create this file if it doesn't exist
pip freeze > requirements.txt

# Install dependencies
First direct into backend folder 
pip install -r requirements.txt

# Or install them manually
# pip install Flask Flask-Cors requests
```

### 3. Download the AI Model

Pull the Gemma model using Ollama. This project is configured for `gemma:1b` (a good balance), but you can use other variants.

```bash
ollama run gemma:1b
```
*(This will download the model, which may take a few minutes and several gigabytes of disk space.)*

## 🏃‍♀️ Running the Application

You will need to have **three terminal windows** open.

**Terminal 1: Start Ollama**

Ensure the Ollama application is running. On macOS and Windows, it usually runs in the background with a menu bar/system tray icon. If not, start it from your applications folder.

**Terminal 2: Start the Backend API**

In your project's root directory (`cooking-chatbot`), run the Flask application.

```bash
# Make sure your virtual environment is active
python backend/app.py
```
You should see output indicating the server is running on `http://localhost:5000`.

**Terminal 3: Start the Frontend Server**

Navigate to the `frontend` directory and start Python's built-in HTTP server.

```bash
cd frontend
python -m http.server 8000
```

**Step 4: Access the Chatbot**

Open your web browser and go to:

**http://localhost:8000**

You can now start chatting with your cooking assistant!

## 📁 Project Structure

```
cooking-chatbot/
├── backend/
│   └── app.py          # Flask API server
├── frontend/
│   ├── index.html      # Main HTML structure
│   ├── script.js       # JavaScript for API communication and UI logic
│   └── style.css       # All styles for the application
├── venv/               # Python virtual environment
└── README.md           # This file
```