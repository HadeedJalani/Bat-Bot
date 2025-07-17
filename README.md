# BAT-BOT: A Smart WhatsApp Chatbot

BAT-BOT is a conversational WhatsApp bot I built using Python (Flask), integrated with Google's Gemini AI. It supports multiple languages, remembers context for better replies, and can be easily personalized. I originally created it as a personal project to experiment with real-time AI interactions over WhatsApp.

## Features

* Context-aware conversations (remembers previous messages)
* Detects and responds in different languages like English, Urdu, Arabic, and French
* Connects to the Gemini API for intelligent, dynamic responses
* Works with Twilio’s WhatsApp API for two-way messaging
* Optional React-based UI for testing and sending messages
* Configurable persona with memory and custom behavior
* Secrets and API keys are handled securely via `.env`

## Tech Stack

* Python (Flask) – backend framework
* Twilio – handles WhatsApp message delivery
* Google Gemini API – for generating responses
* langdetect – to auto-detect the user's language
* dotenv – for environment variable management
* React (optional) – frontend interface built with Tailwind CSS

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/HadeedJalani/Bat-Bot.git
cd Bat-Bot
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory and fill it like this:

```
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
FROM_NUMBER=whatsapp:+14155238886
TO_NUMBER=your_verified_whatsapp_number
GEMINI_API_KEY=your_google_gemini_api_key
```

### 3. Install Python Dependencies

```
pip install -r requirements.txt
```

### 4. Run the Flask App

```
python app.py  # or python webhook.py if that’s your file
```

### 5. Set Up ngrok for Webhook Testing

```
ngrok http 5000
```

Copy the generated URL and set it as your webhook in Twilio:

```
https://your-ngrok-url.ngrok.io/whatsapp
```

## How to Use

Once everything’s running, send a message like:

```
Hey BAT-BOT, who created you?
```

BAT-BOT will reply smartly, in your language, and remember the conversation as it continues.

## About the Creator

This project was built by Hadeed Jalani. I’m a developer and debate enthusiast who loves building things that combine tech and communication.

Instagram: [https://instagram.com/hadeedjalani](https://instagram.com/hadeedjalani) / [https://instagram.com/hadeedinconflict](https://instagram.com/hadeedinconflict)

## License

This is a public project for educational and demo purposes. Feel free to fork or learn from it, but please don’t redistribute or commercialize it without permission.
