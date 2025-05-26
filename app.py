from flask import Flask, render_template, request, jsonify
from GF import get_response_from_ai, get_voice_message
import os
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        logger.info(f"Received message: {user_message}")
        
        # Get text response
        response = get_response_from_ai(user_message)
        logger.info(f"AI Response: {response}")
        
        # Try to get voice response
        logger.info("Attempting to generate voice response...")
        voice_result = get_voice_message(response)
        
        if voice_result is None:
            logger.warning("Voice generation failed, but continuing with text response")
        else:
            logger.info("Voice generation successful")
        
        return jsonify({'response': response})
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({'error': 'An error occurred while processing your request'}), 500

if __name__ == '__main__':
    # Verify environment variables
    if not os.getenv("ELEVEN_LABS_API_KEY"):
        logger.error("ELEVEN_LABS_API_KEY is not set in environment variables!")
    if not os.getenv("GROQ_API_KEY"):
        logger.error("GROQ_API_KEY is not set in environment variables!")
        
    app.run(debug=True) 