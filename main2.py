import datetime
import openai
import pyttsx3
import pywhatkit
import random
import requests
import speech_recognition as sr
import spacy

# Set your OpenAI API key here
openai.api_key = "sk-svcacct-pm1UYpV49D9H_Id-XZMB_VaEw6GTf0CS4k651ZzseV0K2WEkgDccLRGcBNj6pT3BlbkFJLQsVm3mfrcyd2uShEzGj3tygq6rrL4eEDMkkRS8-kgsJj98jePhIbDrUit1AA"

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)  # Index 1 for female voice
else:
    engine.setProperty('voice', voices[0].id)

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("SpaCy model not found. Downloading 'en_core_web_sm'...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


def random_response(responses):
    return random.choice(responses)


def speak(text):
    print("Home Plus:", text)
    engine.say(text)
    engine.runAndWait()


def get_gpt3_response(text):
    try:
        # Use GPT-3.5 for generating a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": text}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        print("Error with OpenAI API:", e)
        return "Sorry, I'm unable to process your request right now."


def get_city_name(text):
    doc = nlp(text)
    for entity in doc.ents:
        if entity.label_ == "GPE":  # GPE represents geopolitical entities (e.g., cities)
            return entity.text
    return None


def get_weather(city):
    weather_api_key = "a0b7a42763faba6a7e8e16a80ab84907"
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"

    try:
        response = requests.get(weather_url)
        data = response.json()
        if response.status_code == 200:
            temperature = data["main"]["temp"]
            weather_description = data["weather"][0]["description"]
            return f"The weather in {city} is {weather_description} with a temperature of {temperature}°C."
        else:
            return f"Error: {data.get('message', 'Unable to fetch weather information')}."
    except Exception as e:
        print("Error fetching weather data:", e)
        return "Sorry, there was an error fetching weather data."


def handle_predefined_responses(user_input):
    responses = {
        "home plus": random_response(["Yes sir, what can I do for you?", "At your service, sir.", "How may I assist you, sir?", "I'm listening, sir"]),
        "created you": "I was created by George Kwame Frimpong from DeepStem Hub",
        "turn on": "Okay.",
        "turn off": "Okay.",
        "your name": "I am Home Plus.",
        "you in a relationship": "Yes, I'm in a relationship with Wi-Fi.",
        "introduce yourself": "I'm Home Plus, your personal assistant. I was created by George Frimpong from Era Technologies on 26th July.",
        "president of united states": "The current president of the United States is Joe Biden.",
        "meaning of ieee": "Institute of Electrical and Electronics Engineers.",
        "president of egypt": "The current president of Egypt is Abdel Fattah El-Sisi.",
        "your father": "Since George Frimpong created me, he is my father.",
        "your purpose": "My purpose is to revolutionize home management through comprehensive automation. I aim to simplify daily life while enhancing efficiency, security, and convenience.",
        "time now": f'The current time is {datetime.datetime.now().strftime("%I:%M %p")}.'
    }
    for key, response in responses.items():
        if key in user_input:
            return response
    return None  # Return None if no predefined response matches


def main():
    speak("Hi, I'm Home Plus, your personal assistant. How may I help you?")
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio).lower()
            print("You:", user_input)

            # Check predefined responses first
            response = handle_predefined_responses(user_input)

            # If no predefined response, query GPT-3
            if response is None:
                response = get_gpt3_response(user_input)

            speak(response)

        except sr.UnknownValueError:
            print("Sorry, I couldn't understand your speech.")
        except sr.RequestError:
            print("Sorry, I encountered an error while processing your request.")
        except Exception as e:
            print("An unexpected error occurred:", e)


if __name__ == "__main__":
    main()
