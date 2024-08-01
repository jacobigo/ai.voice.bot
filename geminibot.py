import os
import google.generativeai as genai
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS

mytext = 'Welcome to me'
language = 'en'

os.environ['myKey'] = 'AIzaSyDJW-e_IAn4XESJQUqYYQe1qZ-UvVxlNMI'
genai.configure(api_key=os.environ['myKey'])
load_dotenv()
model = genai.GenerativeModel('gemini-1.5-flash')
# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init("dummy")
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)
name = "Big Papa"
greetings = [f"whats up master {name}",
             "yeah?",
             "Well, hello there, Master of Puns and Jokes - how's it going today?",
             f"Ahoy there, Captain {name}! How's the ship sailing?",
             f"Bonjour, Monsieur {name}! Comment ça va? Wait, why the hell am I speaking French?" ]
def listen_for_wake_word(source):
    print("Listening for 'Hey'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if "hey" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass
def listen_for_keyboard(source):
	while True:
		try:
			scanText = input("Enter 'Hey' to start talking: ")
			if scanText == "Hey":
				engine.runAndWait()
				listen_and_respond(source)
				break
		except sr.UnknownValueError:
			pass

# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            if not text:
            	continue
            # Send input to OpenAI API
            response = model.generate_content(text)
            response_text = response.text
            print(response_text)
            print("generating audio")
            myobj = gTTS(text = response_text, lang = language, slow = False)
            myobj.save("response.mp3")
            print("speaking")
            os.system("vlc response.mp3")
            # Speak the response
            print("speaking")
            engine.say(response_text)
            engine.runAndWait()
	if not audio:
		# listen_for_wake_word(source)
		listen_for_keyboard(source)
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            # listen_for_wake_word(source)
	    listen_for_keyboard(source)
            break
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            # listen_for_wake_word(source)
	    listen_for_keyboard(source)
            break

# Use the default microphone as the audio source
with sr.Microphone() as source:
	# listen_for_wake_word(source)
	listen_for_keyboard(source)
