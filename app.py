from flask import Flask, request, jsonify
from flask import render_template

from flask_cors import CORS
from google.cloud import dialogflow_v2 as dialogflow
from google.cloud.dialogflow_v2.types import TextInput, QueryInput
from google.oauth2 import service_account
import uuid
import json
import requests  # ✅ Required for translation API

app = Flask(__name__)
CORS(app)

# Load Dialogflow service account key
with open("dialogflow_key.json") as f:
    creds_dict = json.load(f)

credentials = service_account.Credentials.from_service_account_info(creds_dict)
session_client = dialogflow.SessionsClient(credentials=credentials)
project_id = creds_dict["project_id"]

SESSION_ID = "smartbot-session-1"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message")
        session = session_client.session_path(project_id, SESSION_ID)

        text_input = dialogflow.types.TextInput(text=user_message, language_code="en")
        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(session=session, query_input=query_input)
        reply = response.query_result.fulfillment_text

        print("✅ BOT REPLY:", reply)
        return jsonify({"reply": reply}), 200

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"reply": "⚠️ Server error: " + str(e)}), 500

# ✅ New route to handle translation via backend


@app.route("/translate", methods=["POST"])
def translate():
    try:
        data = request.json
        text = data.get("text")
        target_lang = data.get("target")

        if not text or not target_lang:
            return jsonify({"error": "Missing input"}), 400

        response = requests.post("https://libretranslate.de/translate", json={
            "q": text,
            "source": "en",
            "target": target_lang,
            "format": "text"
        }, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            translated_text = response.json().get("translatedText")
            return jsonify({"translatedText": translated_text})
        else:
            return jsonify({"error": "Translation API failed"}), 500

    except Exception as e:
        print("❌ Translation Error:", e)
        return jsonify({"error": str(e)}), 500



@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
