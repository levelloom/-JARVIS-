import speech_recognition as sr
import datetime
import subprocess
import pywhatkit  # type: ignore
import pyttsx3
import webbrowser
import os
import sys

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set desired voice here

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to listen and return voice input with noise filtering
def listen_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjusting for noise for 1 second
        print("......J.A.R.V.I.S......")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language='en_US').lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            engine.say("Sorry, I did not understand that.")
            engine.runAndWait()
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say("Sorry, I could not reach the speech recognition service.")
            engine.runAndWait()
            return ""

# Welcome message
def welcome_message():
    welcome_text = "Activation complete. Jarvis at your service, sir."
    engine.say(welcome_text)
    engine.runAndWait()  # Don't forget to run this to actually speak

# Command function to process voice input
def process_command(text):
    global assistant_active  # Use the global variable to check assistant status

    # Respond to "Hey, Jarvis, are you there?"
    if 'hey jarvis are you there' in text:
        engine.say('Activating the system.')
        welcome_message()  # Say welcome message after activation
        assistant_active = True  # Set the assistant to active state
        return

    # If the assistant is not active, ignore other commands
    if not assistant_active:
        return

    # Shutdown command
    if 'shutdown' in text or 'exit' in text:
        engine.say('Shutting down. Goodbye, sir.')
        engine.runAndWait()
        print('Shutting down...')
        sys.exit()

    # Opening Chrome
    elif 'chrome' in text:
        engine.say('Opening Chrome...')
        engine.runAndWait()
        program_name = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if os.path.exists(program_name):
            subprocess.Popen([program_name])
        else:
            engine.say("Sorry, I could not find Chrome on your system.")
            engine.runAndWait()

    # Opening Spotify
    elif 'spotify' in text:
        engine.say('Opening Spotify...')
        engine.runAndWait()
        spotify_path = r"C:\Users\yadav\AppData\Roaming\Spotify\Spotify.exe"
        if os.path.exists(spotify_path):
            subprocess.Popen([spotify_path])
        else:
            engine.say("Sorry, I could not find Spotify on your system.")
            engine.runAndWait()

    # Open System's Media Player (e.g., Windows Media Player or VLC)
    elif 'media player' in text:
        engine.say('Opening the media player...')
        engine.runAndWait()
        media_player_path = r"C:\Program Files\Windows Media Player\wmplayer.exe"
        if os.path.exists(media_player_path):
            subprocess.Popen([media_player_path])
        else:
            vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
            if os.path.exists(vlc_path):
                subprocess.Popen([vlc_path])
            else:
                engine.say("Sorry, I could not find a media player on your system.")
                engine.runAndWait()

    # Check current time
    elif 'time' in text:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        engine.say(f"The time is {current_time}")
        engine.runAndWait()

    # Play a song or video on YouTube
    elif 'play' in text:
        video = text.replace('play', '').strip()
        engine.say(f'Searching and playing {video} on YouTube...')
        engine.runAndWait()
        print(f"Playing {video} on YouTube...")
        pywhatkit.playonyt(video)

    # Opening YouTube
    elif 'youtube' in text:
        engine.say('Opening YouTube...')
        engine.runAndWait()
        webbrowser.open('http://www.youtube.com')

    # Respond to fees inquiry
    elif 'fees' in text or 'fee' in text:
        engine.say('Your fees are 800 rupees.')
        engine.runAndWait()

    # Identify assistant
    elif 'who am i talking to' in text:
        engine.say('You are talking to Jarvis, your assistant.')
        engine.runAndWait()

    # Respond to thanks
    elif 'thank you' in text:
        engine.say('It\'s my pleasure.')
        engine.runAndWait()

# Global variable to track the assistant's active status
assistant_active = False

# Main loop
while True:
    command = listen_command()
    if command:  # Ensure a command is captured
        process_command(command)  # Process the command
