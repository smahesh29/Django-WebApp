# Speech to Text converter by Mahesh Sawant

import pyspeech as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak Anything : ")
    audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You said : {}".format(text))
    except:
        print("Sorry could not recognize your voice")