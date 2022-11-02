import pyttsx3
def Male_Voice(text):
    audio = pyttsx3.init()
    voice = audio.getProperty('voices')
    rate = audio.getProperty('rate')
    audio.setProperty('rate', 140)
    audio.setProperty('Volume', 0.8)
    audio.setProperty('voice', voice[0].id)
    audio.save_to_file(text, 'speech.mp3')
    audio.runAndWait()
def Female_Voice(text):
    audio = pyttsx3.init()
    voice = audio.getProperty('voices')
    rate = audio.getProperty('rate')
    audio.setProperty('rate', 140)
    audio.setProperty('Volume', 0.8)
    audio.setProperty('voice', voice[1].id)
    audio.save_to_file(text, 'speech.mp3')
    audio.runAndWait()
def main():
    try:
        voice = input("Enter voice as Male or Female : ")
        if voice == "Male" :
            fh = open(r"C:\Users\shiba\OneDrive\Desktop\Udemy\Projects\Text to Speech\Text.txt", "r")
            text = fh.read().replace("\n", "  ")
            Male_Voice(text)
            fh.close()
        elif voice == "Female":
            fh = open(r"C:\Users\shiba\OneDrive\Desktop\Udemy\Projects\Text to Speech\Text.txt", "r")
            text = fh.read().replace("\n", "  ")
            Female_Voice(text)
            fh.close()
        else:
            print("Close the Program and run it again. This time use the correct Voice Parameter !!")
    except:
        print("Some internal error has occured. Please close the program and run it again.")
if __name__ == "__main__":
    main()

