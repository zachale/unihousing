import boto3
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the Bedrock client
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# Define the model
model_id = "openai.gpt-oss-20b-1:0"


def extract_description(description: str) -> str:
    messages = {
        "role": "user",
        "content": [{
            "text": description
        }]},
    system=[{
            "text": (
                "You are given the description for a lease posting. Return ONLY a json object containing fields. "
                "DO NOT INCLUDE ANY TEXT. ONLY RETURN THE JSON. Extract the following fields from the description. "
                "Only include fields that are EXCPLICITLY stated.\n\n"
                "demographic: string; // 'woman', 'mixed', 'man', 'null'.\n"
                "term_length: int; // term length in months. if not stated place 'null'\n"
                "term_length_type: string; // 'winter', 'spring', 'summer', 'fall', 'null'\n"
                "furnished: bool; // true / false\n"
                'Ex: "3min walk to the Mall", "12 min bus, or 30 minute walk to Campus"\n'
            )
    }]

    inference_config = {
        "maxTokens": 1000,
    }


    # Make the API call
    response = client.converse(
        modelId=model_id,
        messages=messages,
        system=system,
        inferenceConfig=inference_config,
    )

    json_response = json.loads(response['output']['message']['content'][1]['text'])
    print(json_response)

    # Remove key-value pairs where the value is null
    if isinstance(json_response, dict):
        json_response = {k: v for k, v in json_response.items() if v is not None and v != "null"}

    print(json_response)

    # Return the response text
    return json_response