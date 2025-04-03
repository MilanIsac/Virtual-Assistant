from transformers import pipeline
import speech_recognition as sr
import pyttsx3
import webbrowser
import pyperclip
from gtts import gTTS
import playsound
import os

engine = pyttsx3.init()
engine.setProperty('voice', engine.getProperty('voices')[1].id)

def speak(text):
    tts = gTTS(text=text, lang='hi', slow=False)
    filename = "temp_audio.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Bol...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='hi-in')
        print(f"Tune bola: {query}\n")
    except Exception as e:
        print(f"Error: {e}")
        print("Kya bola samajh nahi aaya...")
        return "None"
    return query.lower()

generator = pipeline('text-generation', model='gpt2')

def get_response(prompt):
    output = generator(prompt, max_length=100, num_return_sequences=1, truncation=True)
    # in generator function, we can set the max_length to control the length of the output, num_return_sequences to control the number of outputs, and truncation to control whether to truncate the input or not.
    return output[0]['generated_text']

def summarize_text(text):
    prompt = f"Summarize the following text: {text}"
    summary = get_response(prompt)
    speak(f"Summary ye rha: {summary}")
    return summary

def get_meaning(word):
    prompt = f"What is the meaning of {word}?"
    meaning = get_response(prompt)
    speak(f"{word} ka matlab hai: {meaning}")
    return meaning


if __name__ == "__main__":
    speak("Bhai bol kya kaam hai?")
    while True:
        query = take_command()

        if "open website" in query:
            speak("Kaunsi website?")
            site = take_command()
            if site != "None":
                if not site.startswith("http"):
                    site = f"https://{site}"
                webbrowser.open(site)
                speak(f"{site} khol diya!")
            else:
                speak("Site ka naam nahi samajh aaya!")

        elif "search" in query:
            speak("Kya search karu?")
            search_query = take_command()
            if search_query != "None":
                search_query = search_query.replace(" ", "+")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                speak(f"{search_query} search kar diya!")
            else:
                speak("Search ke liye kuch samajh nahi aaya!")

        elif "copy" in query:
            speak("Kis cheez ko copy karna hai?")
            text = take_command()
            if text != "None":
                pyperclip.copy(text)
                speak("Copy kar diya!")
            else:
                speak("Copy ke liye kuch samajh nahi aaya!")

        elif "paste" in query:
            pasted = pyperclip.paste()
            speak(f"Paste kar diya: {pasted}")

        elif "bye" in query:
            speak("Ok bye bhai!")
            break