import pyttsx3
import os

def text_to_speech(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set properties before adding anything to speak
    engine.setProperty('rate', 150)    # Speed percent (can go over 100)
    engine.setProperty('volume', 1.0)  # Volume 0-1

    # Save the output as an mp3 file in the 'audio' directory
    output_file = os.path.join("audio", "output.mp3")
    engine.save_to_file(text, output_file)
    engine.runAndWait()

    return "output.mp3"
