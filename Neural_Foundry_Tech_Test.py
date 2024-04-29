import os
import string
import traceback
import warnings

import speech_recognition as sr
import whisper
from pydub import AudioSegment
from urllib3.exceptions import InsecureRequestWarning, SecurityWarning

# Suppress the specific NotOpenSSLWarning from urllib3
warnings.simplefilter('ignore', InsecureRequestWarning)
# Suppress any other Security warnings
warnings.simplefilter('ignore', SecurityWarning)

# Suppress specific UserWarnings from the whisper library
warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")

# Function to convert the speech recorded from the microphone into an MP3 file.
def save_speech_to_mp3(audio, file_path="output.mp3"):
    """
    Purpose:
        This function uses the pydub library to convert the raw audio data captured by
        the speech_recognition library into an MP3 format and saves it to the specified
        path. This file can then be used by the Whisper model for transcription.

    Parameters:
        audio (AudioData): The audio data captured from the microphone.
        file_path (str): The path where the MP3 file will be saved.

    Returns:
        str: The file path of the saved MP3 file.
    """
    
    # Convert the speech recognition audio data to WAV format data using the parameters
    # suitable for conversion to MP3. This includes setting the sample rate to 16000 Hz
    # and the sample width to 2 bytes.
    sound = AudioSegment(
        data=audio.get_wav_data(
            convert_rate=16000,  # Set the sample rate to 16000 Hz for MP3 encoding
            convert_width=2      # Set the sample width to 2 bytes
        )
    )
    
    # Export the audio data as an MP3 file to the specified file path.
    # The format is explicitly set to "mp3" to ensure the correct encoding.
    sound.export(file_path, format="mp3")
    
    # Return the path to the saved MP3 file, allowing it to be used elsewhere in the application.
    return file_path



# Function to convert text to
# speech
def SpeakText(command):
    """
    Purpose:
        This function takes a text string and uses macOS's built-in text-to-speech
        capabilities to vocalize it. It is useful for auditory feedback or for
        accessibility purposes.

    Parameters:
        command (str): The text string to be converted into speech.

    Return Value:
        None: This function does not return any value, it only initiates speech output.
    """
    os.system(f'say "{command}"')

# Function to map recognized text to JSON formatted actions
def map_text_to_action(text):
    '''
    Purpose:
        To convert a simple spoken command into a structured JSON object that defines
        a specific action, making it easier to interpret and execute commands programmatically.

    Parameters:
        text (str): The text string that contains the command to be mapped.

    Return Value:
        dict: A dictionary representing the action to be taken. If the command is recognized,
              it returns the corresponding JSON object; if not, it returns a JSON object with
              an "error" key indicating the command is unknown.
    '''
    # Clean the text by removing punctuation and converting to lower case
    text = text.lower().strip()
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Define a dictionary mapping recognized text to JSON formatted actions
    actions = {
        'move forward': {'direction': 'linear', 'quantity': 1},
        'move backwards': {'direction': 'linear', 'quantity': -1},
        'turn left': {'direction': 'angular', 'quantity': -1},
        'turn right': {'direction': 'angular', 'quantity': 1}
    }
    # Return the corresponding action for the input text, or an error message if not recognized
    return actions.get(text, {"error": "unknown command"})

# Function to recognize and process the command given by the user
def recognize_and_process_command():
    '''
    Purpose:
        To automate the process of converting spoken commands into actionable data in a JSON format,
        facilitating easy integration with other systems or components that execute the commands.

    Parameters:
        None

    Return Value:
        None: The function prints the recognized command and the resulting action or error directly.
              It does not return any values but directly influences the program by outputting to the console.

    Note:
        This function depends on a microphone for input and requires the Whisper model to be correctly
        initialized and available. It handles exceptions by printing error messages to the con