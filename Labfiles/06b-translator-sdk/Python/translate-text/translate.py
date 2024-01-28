from dotenv import load_dotenv
import os

# import namespaces
from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        translator_region = os.getenv('TRANSLATOR_REGION')
        translator_key = os.getenv('TRANSLATOR_KEY')

        # Create client using endpoint and key
        credential = TranslatorCredential(translator_key, translator_region)
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

         # Translate text
        input_text = ""
        while input_text.lower() != "quit":
            input_text = input("Enter text to translate ('quit' to exit):")
            if input_text != "quit":
                input_text_elements = [InputTextItem(text=input_text)]
                translation_response = client.translate(content=input_text_elements, to=[target_language])
                translation = translation_response[0] if translation_response else None
                if translation:
                    source_language = translation.detected_language
                    for translated_text in translation.translations:
                        print(f"'{input_text}' was translated from {source_language.language} to {translated_text.to} as '{translated_text.text}'.")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()