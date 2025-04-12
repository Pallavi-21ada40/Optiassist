from flask import Flask, render_template, request, jsonify
from chatbot_logic import get_gemini_response  # Import your chatbot logic
from gtts import gTTS
import os
import speech_recognition as sr
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.get_json().get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        user_message_lower = user_message.lower()
        
        # Check for "current time"
        if "current time" in user_message_lower:
            current_time = datetime.now().strftime("%I:%M %p")
            bot_response = f"The current time is {current_time}."
        
        # Check for "current date"
        elif "current date" in user_message_lower:
            current_date = datetime.now().strftime("%B %d, %Y")
            bot_response = f"Today's date is {current_date}."
        
        # Default chatbot logic
        else:
            # Get response from Gemini AI
            bot_response = get_gemini_response(user_message)

        # Convert bot response to speech
        tts = gTTS(text=bot_response, lang='en')
        audio_file = "response.mp3"
        tts.save(audio_file)

        # Return text and audio
        return jsonify({"response": bot_response, "audio_file": audio_file})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/speech_to_text", methods=["POST"])
def speech_to_text():
    recognizer = sr.Recognizer()
    try:
        # Receive audio file from frontend
        audio_file = request.files['audio']
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.record(source)

        # Convert speech to text
        user_message = recognizer.recognize_google(audio_data)

        user_message_lower = user_message.lower()
        
        # Check for "current time"
        if "current time" in user_message_lower:
            current_time = datetime.now().strftime("%I:%M %p")
            bot_response = f"The current time is {current_time}."
        
        # Check for "current date"
        elif "current date" in user_message_lower:
            current_date = datetime.now().strftime("%B %d, %Y")
            bot_response = f"Today's date is {current_date}."
        
        # Default chatbot logic
        else:
            # Get response from Gemini AI
            bot_response = get_gemini_response(user_message)

        # Convert bot response to speech
        tts = gTTS(text=bot_response, lang='en')
        audio_file = "response.mp3"
        tts.save(audio_file)

        return jsonify({"response": bot_response, "user_message": user_message, "audio_file": audio_file})
    except sr.UnknownValueError:
        return jsonify({"error": "Sorry, I couldn't understand the speech."}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"Speech recognition error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
