import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

def process_command(command):
    # Dummy implementation for command processing
    if "hello" in command:
        response = "Hello! How can I help you today?"
    elif "weather" in command:
        response = "I can't check the weather right now, but you can look it up online."
    elif "time" in command:
        from datetime import datetime
        now = datetime.now().strftime("%H:%M:%S")
        response = f"The current time is {now}."
    else:
        response = "Sorry, I didn't understand that command."
    return response

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print("Command received:", command)
            response = process_command(command)
            engine.say(response)
            engine.runAndWait()
            text_var.set(response)
        except sr.UnknownValueError:
            text_var.set("Sorry, I could not understand the audio.")
        except sr.RequestError:
            text_var.set("Sorry, there was an error with the speech recognition service.")

# GUI setup
root = tk.Tk()
root.title("Voice Assistant")

text_var = tk.StringVar()

frame = tk.Frame(root)
frame.pack(pady=20)

label = tk.Label(frame, textvariable=text_var, wraplength=300)
label.pack()

record_button = tk.Button(frame, text="Start Listening", command=listen_command)
record_button.pack(pady=10)

root.mainloop()
