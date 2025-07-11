import speech_recognition as sr # used for recognition of users voice
import webbrowser #to access web
import pyjokes  #to add joke features
from gtts import gTTS #to add voice assistant
import playsound
import os
import random #to generate random  values
import sys #to access files on my pc
import wikipedia #to access wiki
import datetime #to tell date and time
import openai #to integrate chatgpt
import requests #to add news feature
from dotenv import load_dotenv
load_dotenv()

#to initialise voice asssistant using google sound and track
def speak(text):
    print(f"Speaking: {text}")
    tts = gTTS(text=text, lang='en')
    filename = f"voice_{random.randint(1,10000)}.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

recogniser = sr.Recognizer()#object to access speech recognition class

#to integrate chatgpt
openai.api_key = os.getenv("OPENAI_API_KEY") #create .env file and add it to .gitignore with your original API Key

openai.api_key = os.getenv("OPENAI_API_KEY")
def chat_with_gpt(prompt):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Stella, a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response.choices[0].message.content
        return reply.strip()
    except Exception as e:
        print("ChatGPT Error:", e)
        return "Sorry, I couldn't get a response from ChatGPT."
#function to add a news feature using news api
def get_news():
    news_api_key = os.getenv("my_news_api_key")  #get from https://newsapi.org by making an account
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={news_api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        headlines = data["articles"][:10]  # Top 10 headlines

        if headlines:
            speak("Here are the top news headlines:")
            for i, article in enumerate(headlines, 1):
                speak(f"Headline {i}: {article['title']}")
        else:
            speak("Sorry, I couldn't find any headlines.")
    except Exception as e:
        print("News Error:", e)
        speak("Sorry, I couldn't fetch the news.")

#function to make a google search
def googleSearch(q):
    webbrowser.open(f"https://www.google.com/search?q={q}")

#in mood for a joke ? feature is here
def jokes():
    j = pyjokes.get_joke()
    print(f"Joke: {j}") 
    speak(j)

#to act on each command
def processCommand(c):

    #to open google
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    
    #to open youtube
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    
    #to open linkedin
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    
    #to make a google search
    elif "search" in c.lower():
        query = c.lower().replace("search","").strip()
        speak(f"Searching for {query}")
        googleSearch(query)
    
    #to make a youtube search
    elif "search youtube for" in c.lower():
        query = c.lower().replace("search youtube for", "").strip()
        if query:
            speak(f"Searching YouTube for {query}")
            webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        else:
            speak("Please say what you want to search on YouTube.")

    #to listen to a joke
    elif "joke" in c.lower():
        jokes()
    
    #to shutdown the system
    elif "shutdown" in c.lower() or "shut down" in c.lower():
        speak("Are you sure you want to shut down the system? Say yes to confirm.")
        with sr.Microphone() as source:
            confirm_audio = recogniser.listen(source, timeout=5, phrase_time_limit=3)
            try:
                confirm = recogniser.recognize_google(confirm_audio).lower()
                if "yes" in confirm:
                    speak("Shutting down the system. Goodbye!")
                    os.system("shutdown /s /t 5")
                else:
                    speak("Shutdown cancelled.")
            except Exception:
                speak("Sorry, I didn't catch that. Shutdown cancelled.")

    #to restart the system
    elif "restart" in c.lower() or "reboot" in c.lower():
        speak("Restarting the system. See you soon!")
        os.system("shutdown /r /t 5")
    
    #to quit the program
    elif "quit" in c.lower():
        speak("goodbye boss")
        sys.exit()
    
    #to open any file on the system
    elif "open file" in c.lower():
        speak("which file do you want me to open")
        with sr.Microphone() as source:
            audio = recogniser.listen(source)
            filename = recogniser.recognize_google(audio).strip()
            file_path = f"C:/Users/YourUsername/Documents/{filename}"
        if os.path.isfile(file_path):
            speak(f"Opening {filename}")
            os.startfile(file_path)
        else:
            speak("Sorry, I could not find that file.")
    
    #access to wikipedia to summarise
    elif "wikipedia" in c.lower() or "who is" in c.lower() or "what is" in c.lower():
        query = c.lower().replace("what is", "").replace("who is", "").strip()
        result = wikipedia.summary(query, sentences=2)#to limit the answer to two sentence
        speak(result)
    
    #flip a coin
    elif "flip a coin" in c.lower():
        result = random.choice(["Heads", "Tails"])
        speak(f"It's {result}")
    
    #roll a dice
    elif "roll a dice" in c.lower():
        result = random.randint(1,6)
        speak(f"It's {result}")

    #tell  time
    elif "time" in c.lower():
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")

    #tell date 
    elif "date" in c.lower():
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")

    #to ask chatgpt
    elif "ask chat" in c.lower() or "talk to chatgpt" in c.lower() or "ask AI" in c.lower():
        speak("What do you want to ask ChatGPT?")
        with sr.Microphone() as source:
            try:
                user_audio = recogniser.listen(source, timeout=5, phrase_time_limit=8)
                user_question = recogniser.recognize_google(user_audio)
                speak("Let me think...")
                gpt_reply = chat_with_gpt(user_question)
                print("ChatGPT:", gpt_reply)
                speak(gpt_reply)
            except Exception as e:
                print("Error:", e)
                speak("Sorry, I didn't understand that.")

    #to listen to news
    elif "news" in c.lower() or "headlines" in c.lower():
        get_news()




if __name__ == "__main__":
    speak("Initializing stella.....")
    while True:
        #listen for the calling word
        #take initialization from the user

        r = sr.Recognizer()

        # recognise speech 
        print("recognising....")# to check how much time it takes to recognise your voice after listening is initialised
        try:
            with sr.Microphone() as source:
                print("Listening....")
                audio = r.listen(source,timeout=5,phrase_time_limit=3)

            word = r.recognize_google(audio)
            if "stella" in word.lower():
                speak("Yes Sire")
                #listen for command
                with sr.Microphone() as source:
                    print("stella Active ....")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))