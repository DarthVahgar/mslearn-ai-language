from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk

def main():
    global speech_config

    try:
        # Get Configuration Settings
        load_dotenv()
        ai_key = os.getenv('SPEECH_KEY')
        ai_region = os.getenv('SPEECH_REGION')

        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(ai_key, ai_region)
        print('Ready to use speech service in: ', speech_config.region)

        # Get spoken input from microphone
        command = transcribe_command_microphone()
        if command.lower() == 'what time is it?':
            tell_time()

    except Exception as ex:
        print(ex)

def transcribe_command_microphone():
    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('Speak now...')

    # Process speech input and return transcribed command
    return recognize_speech(speech_recognizer=speech_recognizer)

def recognize_speech(speech_recognizer):
    # Process speech input
    # Here, recognize_once() listens for an input utterance from the microphone
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)

    # Return the command
    return command

def tell_time():
    now = datetime.now()
    input_text = 'The time is {:02d}:{:02d}'.format(now.hour, now.minute)

    # Configure speech synthesis
    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural" # Indian voice: en-IN-PrabhatNeural
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config, audio_config)

    # Synthesize spoken output and play / print it
    """
    Here, speak_text_async() converts the given input text to speech
    and sends it to the channel specified in the audio config (i.e., device speaker)
    """
    print("Playing speech response: ")
    speak = speech_synthesizer.speak_text_async(input_text).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)

    # Synthesize spoken output via SSML and play / print it
    print("\nPlaying SSML speech response: ")
    input_ssml = " \
     <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'> \
         <voice name='en-GB-LibbyNeural'> \
             {} \
             <break strength='strong'/> \
             Time to end this lab! \
         </voice> \
     </speak>".format(input_text)
    speak = speech_synthesizer.speak_ssml_async(input_ssml).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)

    # Print the response
    print(input_text)


if __name__ == "__main__":
    main()