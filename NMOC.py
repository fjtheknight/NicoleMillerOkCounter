import random
import time
import speech_recognition as sr
from pynput.keyboard import Key, Controller

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

def count_occurrences(word, sentence):
    return sentence.lower().split().count(word)

# Main:
keyboard = Controller()
print('OKAY robot v0.000001 by fjtheknight')
t0= time.clock()
counter = 0

while True:

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    guess = recognize_speech_from_mic(recognizer, microphone)

    print('Say something')

    try:

        print(guess["transcription"])
        c=count_occurrences('okay', guess["transcription"])
        print(c)
        if c != 0:
            t1 = time.clock() - t0
            keyboard.type('OKAY bot v0.1: Nicole said OKAY '+str(c)+' times in the last '+str(int(t1))+' seconds')
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            counter+=c
            keyboard.type('Total : '+str(counter))
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            t0= time.clock()

    except AttributeError:
        # API was unreachable or unresponsive
        print("AttributeError")


