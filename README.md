# AI Girlfriend Chat Application

An interactive chat application that simulates a conversation with an AI girlfriend using natural language processing and text-to-speech capabilities.

## Features

- Natural language conversation using Groq LLM
- Text-to-speech conversion using ElevenLabs API
- Real-time audio playback
- Web-based chat interface

## Prerequisites

- Python 3.8 or higher
- Groq API key
- ElevenLabs API key

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd AI-girlfriend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your API keys:
```
GROQ_API_KEY=your_groq_api_key
ELEVEN_LABS_API_KEY=your_elevenlabs_api_key
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Start chatting with your AI girlfriend!

## Project Structure

```
AI-girlfriend/
├── app.py              # Main Flask application
├── GF.py              # AI and voice processing logic
├── static/            # Static files (CSS, JS)
├── templates/         # HTML templates
├── audio_files/       # Temporary audio files
├── requirements.txt   # Project dependencies
└── .env              # Environment variables (not tracked in git)
```

## License

MIT License

## Contributing

Feel free to submit issues and enhancement requests! 