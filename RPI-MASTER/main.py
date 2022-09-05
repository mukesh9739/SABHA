import aiy.audio
import aiy.cloudspeech
import aiy.voicehat

import logging
import platform
import sys

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
from google.assistant.library.event import EventType

import RPI.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26,GPIO.OUT)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

def process_event(event):
    status_ui = aiy.voicehat.get_status_ui()
    if event.type == EventType.ON_START_FINISHED:
        status_ui.status('ready')
        if sys.stdout.isatty():
            print('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        status_ui.status('listening')
        recognizer = aiy.cloudspeech.get_recognizer()
        recognizer.expect_phrase('turn on the light')
        recognizer.expect_phrase('turn off the light')
        text = recognizer.recognize()
        if 'turn on the light' in text:
              print (“hi”)
              GPIO.output(26,GPIO.HIGH)
        if 'turn off the light' in text:
              print(“hello”)
              GPIO.output(26,GPIO.LOW)

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        status_ui.status('thinking')

    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        status_ui.status('ready')

    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)

def main():
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn off the light')
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('blink')

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()

    while True:
        print('Press the button and speak')
        button.wait_for_press()
        print('Listening...')
        text = recognizer.recognize()
        if not text:
            print('Sorry, I did not hear you.')
        else:
            print('You said "', text, '"')
            if 'turn on the light' in text:
                led.set_state(aiy.voicehat.LED.ON)
            elif 'turn off the light' in text:
                led.set_state(aiy.voicehat.LED.OFF)
            elif 'blink' in text:
                led.set_state(aiy.voicehat.LED.BLINK)
            elif 'goodbye' in text:
                break
            else
                credentials = aiy.assistant.auth_helpers.get_assistant_credentials()                                  	      with Assistant(credentials) as assistant:
                for event in assistant.start():
                        process_event(event)

if __name__ == '__main__':
    main()
