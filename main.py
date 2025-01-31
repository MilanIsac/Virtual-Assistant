import os
import datetime
import openai
import pyttsx3
import speech_recognition as sr
import time
import requests
import smtplib

openai.api_key = os.getenv("OPEN_API_KEY")

# print(openai.api_key)

engine = pyttsx3.init()

def speak(text):
    # speak("Hello, I am your virtual assistant!")
    # print(text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...", )
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
        
        try:
            print("Recgnizing...")
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}\n")
            return command
        except sr.WaitTimeoutError:
            print("Listening timed out. No audio detected")
            return None 
        except Exception as e:
            print("Could not understand audio")
            return None
        
def nlp_query(query):
    response = openai.Completion.create(
        engine="davinci",
        prompt=query,
        max_tokens=100,
        temperature=0.5
    )
    answer = response.choices[0].text.strip()
    return answer

def main():
    speak("Hello, I am your virtual assistant!")
    
    while True:  # Keeps listening for commands in a loop
        command = listen()
        
        if command is None:
            speak("Can't understand")  # If no command was recognized, go back to listening

        elif "search" in command:
            query = command.split("search")[-1].strip()
            answer = nlp_query(query)
            speak(answer)

        elif "exit" in command:  # Example exit condition
            speak("Goodbye!")
            break  # Exit the loop and end the program

        else:
            speak(f"You said: {command}")

if __name__ == "__main__":
    main()