import logging
import os

import openai
from pymongo import MongoClient

DB_NAME = os.environ.get("DB_NAME")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")

ANSWER_PROMPT: str = r"""You are an assistant that answers questions based on ' \
                   f'sources provided. If the information is not in the' \
                   f' provided source, you answer with "I don\'t know" based 
                   on this information: Based on this information: 

<<<CONTEXT>>>

Answer the following question, if you don't know, then say so and take it step by step:

<<<QUERY>>>

"""


def setup_azureopenai():
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    openai.api_type = os.environ.get("OPENAI_API_TYPE")
    openai.api_base = os.environ.get("OPENAI_API_BASE")
    openai.api_version = os.environ.get("OPENAI_API_VERSION")
    logging.info('azure openai service ready')


def setup_cosmos_connection():
    cosmosclient = MongoClient(os.environ.get("CosmosConnectionString"))
    db = cosmosclient[DB_NAME]
    collection = cosmosclient[DB_NAME][COLLECTION_NAME]
    # Send a ping to confirm a successful connection
    try:
        cosmosclient.admin.command('ping')
        logging.info("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    return collection, db


setup_azureopenai()
collection, db = setup_cosmos_connection()


def create_embeddings(text):
    """Get the embedding for the text."""

    text = text.replace("\n", " ")
    embeddings = openai.Embedding.create(
        input=[text], deployment_id=os.environ.get("OPENAI_DEPLOYMENT_NAME")
    )["data"][0]["embedding"]
    return embeddings


def create_index():
    # delete and recreate the index. This might only be necessary once.
    collection.drop_indexes()
    embedding_len = 1536
    logging.info(f'creating index with embedding length: {embedding_len}')

    db.command({
        'createIndexes': COLLECTION_NAME,
        'indexes': [
            {
                'name': 'vectorSearchIndex',
                'key': {
                    "vectorContent": "cosmosSearch"
                },
                'cosmosSearchOptions': {
                    'kind': 'vector-ivf',
                    'numLists': 100,
                    'similarity': 'COS',
                    'dimensions': embedding_len
                }
            }
        ]
    })

    logging.info("Indexes created successfully")


def transform_and_update_to_cosmos(messages):
    create_index()
    requests = []

    logging.info("Creating requests to append to cosmos db")
    for message in messages:
        # embedding only subject since  model's maximum context length is 8191 tokens
        doc = {"subject": message.Subject, "body": message.Body,
               "vectorContent": create_embeddings(message.Subject)}
        requests.append(doc)

    logging.info("Inserting content into cosmos db")
    collection.insert_many(requests).inserted_ids
    logging.info("Content inserted successfully to cosmos db")


# Cosmos DB Vector Search API Command
def vector_search(vector_query, max_number_of_results=2):
    results = collection.aggregate([
        {
            '$search': {
                "cosmosSearch": {
                    "vector": vector_query,
                    "path": "vectorContent",
                    "k": max_number_of_results
                },
                "returnStoredSource": True
            }
        }
    ])
    return results


# openAI request - ChatGPT 3.5 Turbo Model
def openai_request(prompt, model_engine='text-davinci-003'):
    
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2000,
        temperature=0,
        top_p=1,
        n=1,
        stream=False,
        logprobs=None,
        stop="\n")

    if 'choices' in response:
        if len(response['choices']) > 0:
            answer = response['choices'][0]['text']
        else:
            answer = 'Opps sorry, you beat the AI this time'
    else:
        answer = 'Opps sorry, you beat the AI this time'

    return answer


def get_response(user_question: str):

    # create the embeddings for the user question
    user_question_embedding = create_embeddings(user_question)

    # search the database for the most similar document
    search_results = vector_search(user_question_embedding, 1)

    # prepare the results for the openai prompt
    result_json = []
    # remove all empty values from the results json
    search_results = [x for x in search_results if x]

    logging.info(f"Total search results: {len(search_results)}")
    for doc in search_results:
        result_json.append(doc.get('body'))
    
    # create the prompt
    prompt = ANSWER_PROMPT.replace("<<<QUERY>>>", user_question)
    prompt = prompt.replace("<<<CONTEXT>>>",
                            result_json[0])
    prompt = prompt.encode(encoding="ASCII", errors="ignore").decode()

    logging.info(f"Prompt: {prompt}")

    # generate the response
    response = openai_request(prompt)
    logging.info(f'User question: {user_question}')
    logging.info(f'OpenAI response: {response}')
    return response

