from dotenv import load_dotenv
import os
import requests, json

# import namespaces
from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem

def main():
    global translator_endpoint
    global cog_key
    global cog_region
    global client

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')
        translator_endpoint = 'https://api.cognitive.microsofttranslator.com'

        # Create client using endpoint and key
        credential = TranslatorCredential(cog_key, cog_region)
        client = TextTranslationClient(credential)

        # Choose target language for translating reviews
        languages_response = client.get_languages(scope="translation")
        print("{} languages supported.".format(len(languages_response.translation)))
        print("Enter a target language code for translation (for example, 'en'):")
        target_language = "xx"
        supported_language = False
        while supported_language == False:
            target_language = input()
            if  target_language in languages_response.translation.keys():
                supported_language = True
            else:
                print("{} is not a supported language.".format(target_language))

        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Translate if not already English
            if target_language != 'en':
                translate(text, target_language)
                
    except Exception as ex:
        print(ex)

def translate(input_text, target_language):
    translation = ''

    # Use the Azure AI Translator translate function
    input_text_elements = [InputTextItem(text=input_text)]
    translation_response = client.translate(content=input_text_elements, to=[target_language])
    translation = translation_response[0] if translation_response else None
    if translation:
        source_language = translation.detected_language
        for translated_text in translation.translations:
            print(f"'{input_text}' was translated from {source_language.language} to {translated_text.to} as '{translated_text.text}'.")

if __name__ == "__main__":
    main()