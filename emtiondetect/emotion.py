import pickle
from gradientai import Gradient
import random
import requests
import pandas as pd

def load_model_adapter_id(file_path):
    with open(file_path, 'rb') as f:
        model_adapter_id = pickle.load(f)
    return model_adapter_id

def retrieve_model_adapter(access_token, workspace_id, model_adapter_id):
    with Gradient(access_token=access_token, workspace_id=workspace_id) as gradient:
        model_adapter = gradient.get_model_adapter(model_adapter_id=model_adapter_id)
    return model_adapter

def get_response(user_input):
    return recommendation_response(user_input.lower())

def recommendation_response(emotion):
    df = pd.read_csv('emtiondetect/data/quote_dataset.csv')
    emotion_label_mapping = {
        'joy': ['Optimism','Gratitude', 'Laughter', 'Happiness', 'Joy'],
        'sadness': ['Resilience', 'Overcoming', 'Grit', 'Patience', 'Rising Above', 'Responsibility',
                    'Courage', 'Perseverance', 'Appreciation', 'Making a Difference', 'Rising Above'],
        'fear': ['Courage', 'Bravery', 'Overcoming', 'Rising Above', 'Determination', 'Rising Above'],
        'surprise': ['Discovery', 'Wonder', 'Imagine'],
        'disgust': ['Integrity', 'Soul'],
        'anger': ['Forgiveness', 'Courage', 'Determination', 'Purpose', 'Right Choices']
    }
    labels = [label.upper() for label in emotion_label_mapping.get(emotion, [])]
    filtered_df = df[df['Category'].isin(labels)]
    if not filtered_df.empty:
        random_entry = random.choice(filtered_df.index)
        image_url = filtered_df.loc[random_entry, 'Image-link']
        return image_url
    else:
        return None

def get_emotion(text_input):
    # Load the model adapter ID from the file
    model_adapter_id = "1dbe795b-cce1-4ed9-9b2f-9738d30842db_model_adapter"

    # Your access token and workspace ID
    access_token = "7Ve3RqWYuLjpfljfe2JM4Z3UCpCArTtW"
    workspace_id = "30132923-499e-46f9-81e5-dbd582d00a96_workspace"

    # Retrieve the model adapter using the ID
    model_adapter = retrieve_model_adapter(access_token, workspace_id, model_adapter_id)

    # Now you can use the model adapter to generate predictions or perform other tasks
    sample_query = "### Instruction: {text_input} \n\n### Response:"
    completion = model_adapter.complete(query=sample_query, max_generated_token_count=100).generated_output
    emotion = completion.split('\n')[0].strip()
    user_input = emotion
    image_url = get_response(user_input)
    if image_url:
        pass
    else:
        print("No quotes found for the provided emotion.")

