from dotenv import load_dotenv
import os

# import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        review_list = []

        language_list = []
        sentiment_list = []
        key_phrase_list = []
        entity_list = []
        linked_entity_list = []
        
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            # print('\n-------------\n' + file_name)
            # print('\n' + text)
            review_list.append(text)

        # Get language
        language_response = ai_client.detect_language(documents=review_list)
        for response in language_response:
            language_list.append(response.primary_language.name)

        # Get sentiment
        sentiment_response = ai_client.analyze_sentiment(documents=review_list)
        for response in sentiment_response:
            sentiment_list.append(response.sentiment)

        # Get key phrases
        key_phrase_response = ai_client.extract_key_phrases(documents=review_list)
        for response in key_phrase_response:
            key_phrase_list.append(response.key_phrases)

        # Get entities
        entity_response = ai_client.recognize_entities(documents=review_list)
        for response in entity_response:
            entity_list.append(response.entities)

        # Get linked entities
        linked_entity_response = ai_client.recognize_linked_entities(documents=review_list)
        for response in linked_entity_response:
            linked_entity_list.append(response.entities)

        # print analysed details about each review
        for index, original_review in enumerate(review_list):
            print(f"{index + 1}.")
            print(f"Original review: {original_review}\n")

            language = language_list[index]
            print(f"Language: {language}\n")

            sentiment = sentiment_list[index]
            print(f"Sentiment: {sentiment}\n")

            key_phrases = key_phrase_list[index]
            print(f"Key phrases: {*key_phrases,}")

            entities = entity_list[index]
            # print(f"Entities: {entities}")
            print(f"Entities: ")
            for entity in entities:
                print("\t{} ({}, {})".format(entity.text, entity.category, entity.subcategory))
            print("\n")

            linked_entities = linked_entity_list[index]
            # print(f"Linked entities: {linked_entities}")
            print("Linked entities:")
            for linked_entity in linked_entities:
                print('\t{} ({})'.format(linked_entity.name, linked_entity.url))
            print("\n\n\n")

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()