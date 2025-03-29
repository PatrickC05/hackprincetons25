from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents="Give me a summary of Agilent Technologies, what they do, how they make money, and their future outlook in 3 sentences."

        )
        print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")
else:
    print("GEMINI_KEY environment variable not set.")