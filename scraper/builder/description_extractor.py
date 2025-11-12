from __future__ import annotations

import json
import logging
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the Bedrock client
client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# Define the model
model_id = "openai.gpt-oss-20b-1:0"

logger = logging.getLogger(__name__)


def extract_description(description: str) -> dict[str, Any]:
    if not description or not description.strip():
        return {}

    messages = [
        {
            "role": "user",
            "content": [{"text": description}],
        }
    ]

    system = [
        {
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
        }
    ]

    inference_config = {
        "maxTokens": 1000,
    }

    try:
        response = client.converse(
            modelId=model_id,
            messages=messages,
            system=system,
            inferenceConfig=inference_config,
        )

        content = response.get("output", {}).get("message", {}).get("content", [])
        text_blocks = [
            block.get("text") for block in content if isinstance(block, dict) and block.get("text")
        ]
        raw_payload = next((text for text in text_blocks if text.strip()), "")
        if not raw_payload:
            return {}

        json_response = json.loads(raw_payload)
    except (BotoCoreError, ClientError) as exc:
        logger.info("Bedrock description extraction failed: %s", exc, exc_info=True)
        return {}
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
        logger.info("Unable to parse description extraction payload: %s", exc, exc_info=True)
        return {}

    if isinstance(json_response, dict):
        return {k: v for k, v in json_response.items() if v is not None and v != "null"}

    return {}
