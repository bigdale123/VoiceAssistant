import playsound
import os
import speech_recognition as sr
import pyaudio
from datetime import datetime
import json, urllib.request, urllib.parse
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('volume',1.0)
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
engine.setProperty('rate',135)

# NOTICE: The bulk of this code is not mine, but adapted from a guide available at geeksforgeeks.org

def assistant_Speaks(output):
    print("TransitPoint: ", output)

    engine.say(output)
    engine.runAndWait()

def get_audio():
    rObject = sr.Recognizer()
    audio = ''
    text = ''

    while text.lower() not in ["hey transit point","a transit point","a transit van","pay transit point","patrons point","hater"]:
        with sr.Microphone() as source:
            audio = rObject.listen(source, phrase_time_limit = 6)
            try:
                text = rObject.recognize_google(audio, language="en-US")
                print("You: "+str(text.lower()))
            except:
                text = " "
    assistant_Speaks("Yes?")
    with sr.Microphone() as source:
        audio = rObject.listen(source, phrase_time_limit = 12)
    try:
        text = rObject.recognize_google(audio, language="en-US")
        print("You: "+str(text))
        return text
    except:
        return 0


def process_text(input):
    # try:
    print(input)
    if "open application" in input:
        index = input[17:]

    elif ("how do i get to" or "directions to") in input.lower():
        destination = ""
        words = input.split("to")
        destination = words[1]
        destination = destination[1:]
        #print(destination)

        start = "UAB Mini Park, Birmingham, AL"
        finish = destination
        try:
            url_encode = 'https://maps.googleapis.com/maps/api/directions/json?%s' % urllib.parse.urlencode((
                        ('origin', start),
                        ('destination', finish),
                        ('mode', 'transit'),
                        ('transit_mode', 'bus'),
                        ('key', 'AIzaSyBCrqIZe5yq3h8h-Ce9Khrt0ofLMtftPYs')
             ))
            print(url_encode)
            data = {}
            with urllib.request.urlopen(url_encode) as url:
                data = json.loads(url.read().decode())
            steps = dict(data["routes"][0])
            steps = steps["legs"][0]
            steps = steps["steps"]
            for i in steps:
                text = i['html_instructions']
                if "bus" in text.lower():
                    text = "Take the "+i["transit_details"]["line"]["short_name"]+" bus headed to "+i["transit_details"]["headsign"]+" And get off at "+i["transit_details"]["arrival_stop"]["name"]
                    text_1 = "Wait at "+i["transit_details"]["departure_stop"]["name"]+" For a bus headed to "+i["transit_details"]["headsign"]
                    assistant_Speaks(text_1)
                assistant_Speaks(text)
        except:
            assistant_Speaks("I'm sorry, You can not get there by bus.")


if __name__ == "__main__":
    while(1):
        text = get_audio()
        if text == 0:
            continue

        elif "quit" in text:
            assistant_Speaks("Goodbye.")
            break

        else:
            process_text(text)
