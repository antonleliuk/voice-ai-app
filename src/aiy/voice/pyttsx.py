import pyttsx3

engine = pyttsx3.init()

rate = engine.getProperty('rate')   # getting details of current speaking rate
# engine.setProperty('rate', 150)

volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
# engine.setProperty('volume', 0.5)

voices = engine.getProperty('voices')

target_voice = None

for voice in voices:
    if voice.id == "russian":
        target_voice = voice
        break
engine.setProperty('voice', target_voice.id)

def say(text, rate=150, volume=0.3):
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    engine.say(text)
    engine.runAndWait()
    engine.stop()