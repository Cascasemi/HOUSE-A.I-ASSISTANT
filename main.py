import datetime

import openai
import pyttsx3
import pywhatkit
import random
import speech_recognition as sr

# Set your OpenAI API key here
openai.api_key = "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"

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Index 1 for female voice

def random_response(responses):
    return random.choice(responses)

def speak(text):
    print("Home Plus:", text)
    engine.say(text)
    engine.runAndWait()

def get_gpt3_response(text):
    # Use GPT-3 to generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
    )
    return response.choices[0].text.strip()

def main():
    responses_home_plus = ["Yes sir, what can I do for you?", "At your service, sir.", "How may I assist you, sir?", "I'm listening, sir"]
    responses_how_are = ["I'm doing well. How are you?", "Feeling great, sir. What of you?", "I'm having a great day. How are you?",
                           "I'm listening, sir"]
    speak("Hi, I'm Home Plus, your personal assistant. How may I help you")
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio).lower()
            print("You:", user_input)

            response = get_gpt3_response(user_input)

            if "home plus" in user_input:
                response = random_response(responses_home_plus)
            elif "created you" in user_input:
                response = "I was created by George Kwame Frimpong from Era technologies."
            elif "turn on" in user_input:
                response = "Okay"
            elif "Hello" in user_input:
                response = "Hi, I'm Home Plus, your personal assistant. How may I help you"
            elif "turn off" in user_input:
                response = "Okay"
            elif "your name" in user_input:
                response = "I am Home Plus."
            elif "you in a relationship" in user_input:
                response = "Yes,I'm in a relationship with Wi-Fi."
            elif "president of United States" in user_input:
                response = "The current president of the United States is Joe Biden"
            elif "president of USA" in user_input:
                response = "The current president of the United States is Joe Biden"
            elif "president of United States of America" in user_input:
                response = "The current president of the United States is Joe Biden"
            elif "meaning of I Tripple E" in user_input:
                response = "Institute of Electrical and Electronic Engineers"
            elif "president of egypt" in user_input:
                response = "The current president of Egypt is Abdel Fattah El-Sisi"
            elif "you in relationship" in user_input:
                response = "Yes,I'm in a relationship with Wi-Fi."
            elif "you in any relationship" in user_input:
                response = "Yes,I'm in a relationship with Wi-Fi."
            elif "you single" in user_input:
                response = "No,I'm in a relationship with Wi-Fi."
            elif "egypt competition 2023" in user_input:
                response = "I TRIPPLE E YESIST23"
            elif "your father" in user_input:
                response = "Since George Frimpong created me, he is my father"
            elif "your purpose" in user_input:
                response = "My purpose is to envision revolutionalized home management through comprehensive automation. Our solution integrates lighting, water, security, and more, simplifying daily life while enhancing efficiency, security, and convenience."
            elif "time now" in user_input:
                time = datetime.datetime.now().strftime('%I:%M %p')
                response = ('The current time is ' + time)
            elif "your mother" in user_input:
                response = "Obviously George's girlfriend is my mother"
            elif "play" in user_input:
                song = user_input.replace('play', '')
                response = ('Playing' + song)
                pywhatkit.playonyt(song)
            elif "to listen to" in user_input:
                song = user_input.replace('listen to', '')
                response = ('Playing' + song)
                pywhatkit.playonyt(song)

            speak(response)

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand your speech.")
        except sr.RequestError:
            print("Sorry, I encountered an error while processing your request.")

if __name__ == "__main__":
    main()
