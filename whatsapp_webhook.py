import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import google.generativeai as genai
from collections import defaultdict
from langdetect import detect

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Twilio configuration
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("FROM_NUMBER")
TO_NUMBER = os.getenv("TO_NUMBER")

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Store conversation history per user
user_history = defaultdict(list)

# Detect language of incoming message
def detect_language(text):
    try:
        lang = detect(text)
        print("Detected language:", lang)
        return lang if lang in ["en", "ur", "ar", "fr"] else "en"
    except Exception as e:
        print("Language detection failed:", e)
        return "en"

# Generate response using Gemini
def gemini_chat(user_message, sender_id):
    try:
        user_lang = detect_language(user_message)
        print(f"Language used: {user_lang}")

        system_identity = (
            "You are BAT-BOT, an advanced multilingual AI chatbot created by Hadeed Jalani. "
            "NEVER say you were created by Google. "
            "If asked, always say: 'I was created by Hadeed Jalani.'\n"
            "If someone asks who Hadeed is, reply: 'Hadeed Jalani is a passionate developer, "
            "a debater with various achievements in the MUN circuit, and someone with a hobby of historical intellect.'\n"
            "If someone asks about his Instagram, say: '@hadeedjalani and @hadeedinconflict'.\n"
        )

        lang_instruction = {
            "en": "Only reply in English.",
            "ur": "صرف اردو میں جواب دیں۔",
            "ar": "يرجى الرد باللغة العربية فقط.",
            "fr": "Veuillez répondre uniquement en français."
        }.get(user_lang, "Reply in English.")

        # Retrieve recent chat history
        recent_history = user_history[sender_id][-6:]
        context = "\n".join(
            f"User: {recent_history[i]}" if i % 2 == 0 else f"BAT-BOT: {recent_history[i]}"
            for i in range(len(recent_history))
        )

        prompt = f"{system_identity}\n{lang_instruction}\n{context}\nUser: {user_message}\nBAT-BOT:"
        print("Prompt being sent to Gemini:\n", prompt)

        response = model.generate_content(prompt)
        print("Raw Gemini response object:", response)

        reply_text = getattr(response, "text", "").strip()
        if not reply_text:
            reply_text = "Sorry, I couldn’t generate a response."

        return reply_text
    except Exception as e:
        print("Error during Gemini generation:", e)
        return "AI error: Something went wrong while generating a response."

# Handle incoming messages from WhatsApp
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    try:
        incoming_msg = request.form.get("Body")
        sender = request.form.get("From")
        print(f"Incoming message from {sender}: {incoming_msg}")

        ai_response = gemini_chat(incoming_msg, sender)

        # Clean response and truncate if too long
        ai_response = ai_response.encode("utf-8", errors="ignore").decode()
        if len(ai_response) > 1500:
            ai_response = ai_response[:1495] + "\n[Message truncated]"

        # Small delay for stability
        time.sleep(1)

        # Send response back to WhatsApp
        resp = MessagingResponse()
        reply = resp.message()
        reply.body(ai_response)

        print(f"Response sent: {ai_response}")

        # Store conversation for context
        user_history[sender].append(incoming_msg)
        user_history[sender].append(ai_response)

        return str(resp)
    except Exception as e:
        print("Error while replying to WhatsApp:", e)
        return "Internal Server Error", 500

# Handle messages from React frontend to WhatsApp
@app.route("/send", methods=["POST"])
def send_whatsapp():
    data = request.get_json()
    message = data.get("message", "")

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    try:
        msg = client.messages.create(
            body=message,
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )
        print("Message sent from UI:", message)
        return jsonify({"reply": f"Message sent successfully. SID: {msg.sid}"})
    except Exception as e:
        print("Twilio API error:", e)
        return jsonify({"reply": f"Failed to send message: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000)
