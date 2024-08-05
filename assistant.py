import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import sqlite3
from datetime import datetime

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Connect to SQLite database
conn = sqlite3.connect('commands.db')
c = conn.cursor()

# Create table for storing commands and responses
c.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        command TEXT,
        response TEXT,
        timestamp TEXT
    )
''')
conn.commit()

def process_command(command):
    # Dummy implementation for command processing
    if "hello" in command:
        response = "Hello! How can I help you today?"
    elif "weather" in command:
        response = "I can't check the weather right now, but you can look it up online."
    elif "time" in command:
        now = datetime.now().strftime("%H:%M:%S")
        response = f"The current time is {now}."
    else:
        response = "Sorry, I didn't understand that command."
    
    # Log the command and response to the database
    c.execute('''
        INSERT INTO logs (command, response, timestamp) 
        VALUES (?, ?, ?)
    ''', (command, response, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

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

# Close the database connection when the application exits
conn.close()
