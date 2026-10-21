# AI Assistant

A command-line AI assistant in Python. It runs a local model (Qwen2.5 3B) through Ollama and can use tools to answer questions.

## Features

- Chat in the terminal with memory of earlier messages
- Tool calling: the model can call Python functions by itself
  - `get_current_time` - current date and time
  - `get_city_weather` - weather of any city (wttr.in)
  - `get_user_city` - the user's home city
  - `calculate` - safe math calculator
- Step limit (`MAX_STEPS`) so the tool loop never runs forever
- Chat is saved to `output.json` after every turn
- Clear error message if Ollama is not running

## Tech Stack

Python, Ollama, Qwen2.5:3b, OpenAI Python SDK, python-dotenv, requests

## Project Structure

```
simple_ai_assistant.py   # main chat loop
tools.py                 # tool functions and their JSON schemas
Utilities/utilities.py   # logging helper
.env                     # your settings (not uploaded to GitHub)
```

## Setup

1. Install Ollama and download the model:

```
ollama pull qwen2.5:3b
ollama serve
```

2. Create a virtual environment and install packages:

```
python3 -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv requests
```

3. Create a `.env` file in the project folder:

```
BASE_URL=http://localhost:11434/v1
API_KEY=ollama
MODEL=qwen2.5:3b
```

4. Run:

```
python3 simple_ai_assistant.py
```

Type `exit` to stop.

## Example

```
SujalVerma: what is 12 * (3 + 4)?
Assistant: It is 84.

SujalVerma: weather in my city
Assistant: Bangalore: ⛅️ +24°C
```

## Author

Sujal Verma - [GitHub](https://github.com/sujal1118)