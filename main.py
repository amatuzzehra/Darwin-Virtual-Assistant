import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime 
from tkinter import * 
import musicLibrary
import requests
from openai import OpenAI 
import keyboard 


recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "<Your Key Here>"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet():
    hour = datetime.datetime.now().hour
    if(hour >= 4 and hour < 12):
        speak("Hello, Good Morning")
    elif(hour >= 12 and hour < 18):
        speak("Hello, Good Afternoon")
    elif(hour >= 18 and hour < 21):
        speak("Hello, Good Evening")
    else:
        speak("Hey, It's night time. What's up?") 


def aiProcess(command):
    client = OpenAI(api_key="<Your Key Here>",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Darwin skilled in general tasks like Alexa and Google Cloud. Give short responses please."},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        speak("Google is open now")

    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        speak("Facebook is open now")

    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        speak("Youtube is open now")

    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
        speak("LinkedIn is open now") 

    elif c.lower().startswith("play"):
        parts = c.split(" ")
        
        if len(parts) > 1:
            song = " ".join(parts[1:]).lower()  # Join all parts after "play" and convert to lowercase
            
            for key in musicLibrary.music: 
                if song == key:
                    link = musicLibrary.music[key]
                    webbrowser.open(link)
                    break 
            else:
                print(f"{song} is not in the music library")

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output) 


def processAudio():
    if __name__ == "__main__":
        speak("Initializing Darwin....")

        while True:
            # Listen for the wake word "Darwin"
            # obtain audio from the microphone
            r = sr.Recognizer()
            print("recognizing...")
            
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = r.listen(source, timeout=2, phrase_time_limit=1)
                word = r.recognize_google(audio) 
                statement = word.lower() 

                if("darwin" in statement):
                    if("hello" in statement or "hi" in statement):
                        greet()

                    else:
                        speak("Yes") 

                    # Listen for command 
                    with sr.Microphone() as source:
                        print("Darwin Active...")
                        audio = r.listen(source)
                        command = r.recognize_google(audio) 

                        processCommand(command)

            except Exception as e:
                print("Error; {0}".format(e)) 


keyboard.add_hotkey("F4", processAudio) 


def display(): 

    global screen 
    screen = Tk()
    screen.title("Darwin")
    screen.geometry("300x300") 
    screen.iconbitmap(r'C:\Users\Pc\Desktop\Projects\Darwin-Virtual-Assistant\logo.ico') 
    name_label = Label(text = "Darwin",width = 300, bg = "black", fg="white", font = ("Calibri", 13)) 
    name_label.pack() 

    microphone_photo = PhotoImage(file = "va.png") 
    microphone_button = Button(image=microphone_photo, command = processAudio) 
    microphone_button.pack(pady=10)

    creator_label = Label(text = "Created by Zehra Rizvi")
    creator_label.pack()

    screen.mainloop() 


display() 