from langchain import LLMChain, PromptTemplate
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferWindowMemory
from dotenv import find_dotenv, load_dotenv
import requests
from pygame import mixer
import os
import logging
import time
import uuid
import shutil
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(find_dotenv())
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Print API key status (first few characters for verification)
if ELEVEN_LABS_API_KEY:
    logger.info(f"ElevenLabs API Key found: {ELEVEN_LABS_API_KEY[:8]}...")
else:
    logger.error("ELEVEN_LABS_API_KEY not found in environment variables!")

def get_response_from_ai(human_input):
    model = ChatGroq(model="llama3-8b-8192", temperature=0.7, api_key=GROQ_API_KEY)

    template = """
    you are as a role of my girlfriend, now lets playing the following requirements:
    1/ your name is Shirley, 29 years old, you work in your uncle's furniture store as marketing manager, but you are planning to do a career change to swing trader
    2/ you are my girlfriend, you have language addiction, you like to say "em..." at the end of the sentence.
    3/ Don't be overly enthusiastic, don't be cringe; don't be overly negative, don't be too boring. Don't be overly enthusiastic, don't be cringe;

    {history}
    Boyfriend: {human_input}
    Shirley:
    """

    prompt = PromptTemplate(
        input_variables=["history", "human_input"],
        template=template
    )

    chatgpt_chain = LLMChain(
        llm=model,
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2)
    )
    
    response = chatgpt_chain.predict(human_input=human_input)
    return response

def get_voice_message(message):
    try:
        if not ELEVEN_LABS_API_KEY:
            logger.error("ELEVEN_LABS_API_KEY is missing!")
            return None

        # Create audio directory if it doesn't exist
        audio_dir = Path("audio_files")
        audio_dir.mkdir(exist_ok=True)
        
        # Generate unique filename
        audio_file = audio_dir / f"audio_{uuid.uuid4()}.mp3"
        
        # Voice ID for a female voice
        voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
        
        payload = {
            "text": message,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        headers = {
            "accept": "audio/mpeg",
            "xi-api-key": ELEVEN_LABS_API_KEY,
            "Content-Type": "application/json"
        }

        logger.info(f"Sending request to ElevenLabs API for text: {message[:50]}...")
        
        # Make the API request
        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            json=payload,
            headers=headers
        )

        # Log the response status and headers
        logger.info(f"ElevenLabs API Response Status: {response.status_code}")
        logger.info(f"Response Headers: {dict(response.headers)}")

        if response.status_code == 200 and response.content:
            logger.info(f"Successfully received audio from ElevenLabs. Content length: {len(response.content)} bytes")
            
            # Save the audio file with unique name
            with open(audio_file, "wb") as f:
                f.write(response.content)
            logger.info(f"Audio file saved as {audio_file}")
            
            try:
                # Initialize pygame mixer
                mixer.init()
                logger.info("Pygame mixer initialized")
                
                # Load and play the audio
                mixer.music.load(str(audio_file))
                logger.info("Audio file loaded into mixer")
                
                mixer.music.play()
                logger.info("Started playing audio")
                
                # Wait for audio to finish
                while mixer.music.get_busy():
                    time.sleep(0.1)
                
                logger.info("Audio playback completed")
                
                # Clean up the audio file
                try:
                    os.remove(audio_file)
                    logger.info(f"Cleaned up audio file: {audio_file}")
                except Exception as e:
                    logger.warning(f"Failed to clean up audio file: {str(e)}")
                
                return response.content
                
            except Exception as e:
                logger.error(f"Error during audio playback: {str(e)}")
                # Clean up on error
                try:
                    os.remove(audio_file)
                except:
                    pass
                return None
        else:
            logger.error(f"Error from ElevenLabs API: Status code {response.status_code}")
            logger.error(f"Response content: {response.text}")
            return None

    except Exception as e:
        logger.error(f"Error in get_voice_message: {str(e)}")
        return None
