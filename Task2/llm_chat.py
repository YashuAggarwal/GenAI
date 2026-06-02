from google import genai
from google.genai.errors import ClientError
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("API_Key")
if not api_key:
    raise ValueError("API_Key not found in .env file")

client = genai.Client(api_key=api_key)

def generate_with_retry(client, model, contents, max_retries=5):
    """
    Generate content with automatic retry logic for rate limits and server errors.
    Uses exponential backoff with a maximum of max_retries attempts.
    """
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents
            )
            return response
        except Exception as e:
            error_str = str(e)
            # Check if it's a retryable error (429 rate limit or 503 unavailable)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str or "503" in error_str or "UNAVAILABLE" in error_str:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s, 8s, 16s
                    error_type = "Rate limit" if "429" in error_str else "Service unavailable"
                    print(f"{error_type} error. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    print(f"Max retries ({max_retries}) exceeded. Please try again later.")
                    raise
            else:
                # Re-raise if it's not a retryable error
                raise

user_activity = """
User A logged in and purchased a laptop worth $1200.
User B logged in but did not make any purchase.
User C purchased a phone worth $800.
"""

prompt = f"""
Analyze the following user activity.

{user_activity}

Return ONLY valid JSON in the format below:

{{
    "summary": "",
    "total_users": 3,
    "purchasing_users": 2,
    "total_revenue": 2000,
    "insights": [
        "",
        "",
        ""
    ]
}}
"""

response = generate_with_retry(
    client=client,
    model="gemini-flash-latest",  # Using latest general flash model
    contents=prompt
)

result = response.text.strip()

print("Raw response:")
print(result)
print("\n" + "="*50 + "\n")

# Try to extract JSON if wrapped in markdown code blocks
if result.startswith("```"):
    # Remove markdown code blocks
    result = result.replace("```json", "").replace("```", "").strip()

data = json.loads(result)

print("Parsed JSON:")
print(json.dumps(data, indent=4))