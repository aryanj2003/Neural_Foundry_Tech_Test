**README.md for Neural Foundry Technical Assessment**

---

### Project Overview

This project is a technical assessment for the Neural Foundry Software Engineering position, focusing on creating a simple voice and intent recognition application. The application converts spoken commands into JSON formatted action statements, particularly useful for ROS actions in the command velocity context.

### System Requirements

- Programming Language: Python 3.9 or newer
- Libraries:
  - `speech_recognition` for converting speech to text.
  - `json` for formatting output into JSON.

### Installation

Before running the application, ensure you have Python installed on your system. You can download Python [here](https://www.python.org/downloads/).

To install the necessary Python libraries, run the following command in your terminal:

```bash
pip install SpeechRecognition
```

### Running the Application

To execute the program, follow these steps:

1. Open your command line interface.
2. Navigate to the directory containing the `Neural_Foundry_Tech_Test.py` file.
3. Run the script by typing:

```bash
python Neural_Foundry_Tech_Test.py
```

### How It Works

The application operates in the following manner:

1. Speech to Text: Utilizes the `speech_recognition` library to convert spoken language into text. The application listens for a single phrase or command and processes it into text.
2. Generate Action Statements: Converts the recognized text into a JSON formatted action statement. For example, the command "move forward" is converted to `{"direction": "linear", "quantity": 1}`.

### Code Structure

- The main script `Neural_Foundry_Tech_Test.py` includes functions for speech recognition and JSON conversion.
- Functions are modular, with clear, concise naming conventions that follow the Google Python style guide for readability and maintainability.

### Contributing

If you find any bugs or wish to suggest improvements, please submit an issue or pull request on GitHub. For major changes, please open an issue first to discuss what you would like to change.

### References and Acknowledgements

This project incorporates methodologies and code snippets adapted from the following sources:

- Speech to Text Conversion:
  - The speech recognition functionality in this project was informed by tutorials and examples from GeeksforGeeks. For more detailed       
guidance on implementing speech recognition features in Python, please visit their article: [Python: Convert Speech to Text and Text to Speech](https://www.geeksforgeeks.org/python-convert-speech-to-text-and-text-to-speech/).
- Whisper Model for Speech Recognition:
  - The Whisper model developed by OpenAI was utilized for advanced speech-to-text capabilities. The implementation was guided by the official GitHub repository for Whisper. Detailed documentation and source code can be found here: [OpenAI Whisper GitHub Repository](https://github.com/openai/whisper).
    
These resources were instrumental in the development of this application, providing foundational knowledge and technical methodologies that enhanced the project's capabilities.

### Contact

For any inquiries or further information, please contact Neural Foundry through the official website or the contact form provided there.

### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

This README provides all necessary information to understand, install, and run the application. It is crafted to be clear, concise, and professional, following the guidelines of the Neural Foundry tech assessment.
