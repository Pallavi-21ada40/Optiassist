import requests

def get_gemini_response(user_input):
    # Replace with your actual API key and URL
    API_KEY = "AIzaSyAyc6sMetXcBRrGtYRqwRC4R7eoCtFXb8Y"
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

    headers = {
        "Content-Type": "application/json",
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_input
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(f"{GEMINI_API_URL}?key={API_KEY}", headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()

        # Extract the bot's response text
        return result['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
