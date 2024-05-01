import os
import string
import traceback
import warnings

import speech_recognition as sr
import whisper
from gradientai import Gradient
from pydub import AudioSegment
from urllib3.exceptions import InsecureRequestWarning, SecurityWarning

os.environ['GRADIENT_ACCESS_TOKEN'] = "6FKwYaCTlDfTAARlSJTDjrLjs22AiaJN"
os.environ['GRADIENT_WORKSPACE_ID'] = "ad27a654-5afc-4573-8c66-9674a8313464_workspace"

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
        initialized and available. It handles exceptions by printing error messages to the console.
    '''
    # Load Whisper model
    model = whisper.load_model("base")    
    # Initialize the recognizer
    r = sr.Recognizer()    
     
    # Exception handling to handle
    # exceptions at the runtime
    try:

      # Capture speech input
      with sr.Microphone() as source:
          # wait for a second to let the recognizer
          # adjust the energy threshold based on
          # the surrounding noise level 
          r.adjust_for_ambient_noise(source, duration=0.2)

          SpeakText("Please say a command")
          audio = r.listen(source)  # Listen for the first phrase and extract it into audio data
          print("Speech captured, processing...")


      # Save the captured audio to an MP3 file
      mp3_path = save_speech_to_mp3(audio)
      print("Audio saved to MP3, transcribing...")

      # Transcribe the speech using the Whisper model from the MP3 file
      result = model.transcribe(mp3_path)
      print("Transcription result:", result['text'])
      command_text = result['text']
      
      # Map the recognized text to an action and print the result
      action = map_text_to_action(command_text)
      print(action)

    except sr.RequestError as e:
      print("An error occurred:")
      print(str(e))
      traceback.print_exc()  # This will print the traceback of the exception
        
    except sr.UnknownValueError:
      print("An error occurred:")
      print(str(e))
      traceback.print_exc()  # This will print the traceback of the exception

# Function to orchestrate the training and testing of a model for voice command recognition.
def main():
    """
    Purpose:
        Main execution function to train and test the Gradient AI model on voice commands.

    Parameters:
        None
        
    Return Value:
        None

    Note:
        This function orchestrates the initialization of the Gradient AI model, its training with fine-tuned
        samples, and the testing of the model's ability to accurately recognize and process voice commands.
        Ensure the GRADIENT_ACCESS_TOKEN and GRADIENT_WORKSPACE_ID are correctly set as environment variables
        and that the Gradient AI environment is properly configured before running this function.
    """
    with Gradient() as gradient:
        base_model = gradient.get_base_model(base_model_slug="nous-hermes2")

        # Creating a model adapter to fine-tune
        new_model_adapter = base_model.create_model_adapter(
            name="test model 3"
        )

        # Update this line to dynamically test command variations
        sample_query = f"### Instruction: Recognize any variation of the command 'move forward' such as 'advance', 'go forward', etc., and directly output the corresponding JSON action statement. Do not provide explanations or descriptions. Only the JSON action format is acceptable. Command: 'advance'\n\n### Response: {{'direction': 'linear', 'quantity': 1}}."

        # Before fine-tuning, see how the model handles the command 'advance'
        completion = new_model_adapter.complete(query=sample_query, max_generated_token_count=100).generated_output
        print(f"Generated (before fine-tune): {completion}")


        # Define command variations and their corresponding JSON outputs
        samples = [
            # New entries for 'move forward'
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'move forward'\n\n### Response:",
                "Response": {"direction": "linear", "quantity": 1}
            },
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'advance'\n\n### Response:",
                "Response": {"direction": "linear", "quantity": 1}
            },
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'go forward'\n\n### Response:",
                "Response": {"direction": "linear", "quantity": 1}
            },
            # New entries for 'move backwards'
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'move backwards'\n\n### Response:",
                "Response": {"direction": "linear", "quantity": -1}
            },
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'go back'\n\n### Response:",
                "Response": {"direction": "linear", "quantity": -1}
            },
            # New entries for 'turn left'
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'turn left'\n\n### Response:",
                "Response": {"direction": "angular", "quantity": -1}
            },
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'rotate left'\n\n### Response:",
                "Response": {"direction": "angular", "quantity": -1}
            },
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'make a left turn'\n\n### Response:",
                "Response": {"direction": "angular", "quantity": -1}
            },
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'swivel left'\n\n### Response:",
                "Response": {"direction": "angular", "quantity": -1}
            },
            # New entries for 'turn right'
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'turn right'\n\n### Response:",
                "Response": {"direction": "angular", "quantity": 1}
            },
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'rotate right'\n\n### Response:",
                "Response": {"direction": "angular", "quantity": 1}
            },
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'make a right turn'\n\n### Response:",
                "Response": {"direction": "angular", "quantity": 1}
            },
            {
                "inputs": "### Instruction: Output JSON action for the command. Command: 'swivel right'\n\n### Response:",
                "Response": {"direction": "angular", "quantity": 1}
            }
        ]

        # Fine-tuning the model with command variations
        num_epochs = 100
        for count in range(num_epochs):
            print(f"Fine-tuning the model. Epoch iteration => {count + 1}")
            new_model_adapter.fine_tune(samples=samples)

        # Test the fine-tuned model with an example input
        test_query = input("Enter a command: ")
        completion = new_model_adapter.complete(query=test_query, max_generated_token_count=100).generated_output
        print(f"Test input: '{test_query}' => Output: {completion}")

        # Optionally, clean up by deleting the model adapter after use
        new_model_adapter.delete()

if __name__ == '__main__':
    main()


