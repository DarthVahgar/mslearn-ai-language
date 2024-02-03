from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk
from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem

def main():
    try:
        global speech_config
        global translation_config
        global audio_config

        # Get Configuration Settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure translation config for speech => translated transcription
        translation_config = speech_sdk.translation.SpeechTranslationConfig(ai_key, ai_region)
        translation_config.speech_recognition_language = 'en-US'
        translation_config.add_target_language('fr')
        translation_config.add_target_language('ta')
        translation_config.add_target_language('hi')
        print('Ready to translate from: ', translation_config.speech_recognition_language)

        # Configure speech config for text => speech
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)

        # Get user input
        target_language = ''
        while target_language != 'quit':
            target_language = input('\nEnter a target language\n fr = French\n ta = Tamil\n hi = Hindi\n Enter anything else to stop\n').lower()
            if target_language in translation_config.target_languages:
                translate(target_language)
            else:
                target_language = 'quit'
                

    except Exception as ex:
        print(ex)

def translate(target_language):
    translation = ''

    # Translate speech
    ## Configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config = audio_config)
    print('Speak now...')
    result = translator.recognize_once_async().get()
    print('Translating "{}"'.format(result.text))
    translation = result.translations[target_language]
    print(translation)

    # Synthesize translation
    speech_config.speech_synthesis_voice_name = "en-IN-PrabhatNeural"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)
    print("Playing speech response: ")
    speak = speech_synthesizer.speak_text_async(translation).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)


if __name__ == "__main__":
    main()