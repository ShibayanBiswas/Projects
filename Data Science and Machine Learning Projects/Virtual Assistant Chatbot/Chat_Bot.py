import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Please say something when you see listening... on your screen

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say('I am Alexa. What can I do for you?')
engine.runAndWait()

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
    except Exception as e:
        pass
    return command

def run_alexa():
    command = take_command()
    # Alexa Menu:
    try:
        # To play a song on youtube
        if 'play' in command:
            song = command.replace('play', '')
            talk('playing' + song)
            pywhatkit.playonyt(song)
        # To get the time    
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk('The current time is ' + time)
        # To know about an influential person    
        elif 'who is' in command:
            person = command.replace('who is', '')
            info = wikipedia.summary(person, sentences = 3)
            talk(info)
        # To know about something abstract    
        elif 'what' in command:
            data = command.replace('what', '')
            info = wikipedia.summary(data, sentences = 2)
            talk(info)
        # To hear a joke    
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        # Greetings- 1    
        elif 'hello' in command:
            talk('Hi! Nice to meet you!')
        # Greetings- 2    
        elif 'how are you' in command:
            talk('I am doing good! Thanks for asking!')
        # Stop    
        elif 'stop' in command:
            print("Good Bye!!")
            exit()
        # To be executed if question is not related to the above choices    
        else:
            talk('Please say the command again')
            
    except Exception as e:
        # If information is not there in wikipedia
        talk("Sorry, I don't know the answer to this question. Please try agin!")
        pass

while True:
    run_alexa()
