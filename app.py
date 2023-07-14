import os
import requests
import openai
from flask import Flask, request, jsonify

OPENAI_NAME = os.environ.get("OPENAI_NAME")
OPENAI_KEY = os.environ.get("OPENAI_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION")
OPENAI_SYSTEM_MESSAGE = os.environ.get("OPENAI_SYSTEM_MESSAGE", "You are an AI assistant that helps people find information.")
OPENAI_MAX_TOKEN = int(os.environ.get("OPENAI_MAX_TOKEN", 3000))
OPENAI_TEMPERATURE = int(os.environ.get("OPENAI_TEMPERATURE", 0))
SPEECH_SERVICE_REGION = os.environ.get("SPEECH_SERVICE_REGION")
SPEECH_SERVICE_KEY = os.environ.get("SPEECH_SERVICE_KEY")

openai.api_type = "azure"
openai.api_base = f"https://{OPENAI_NAME}.openai.azure.com/" 
openai.api_version = OPENAI_API_VERSION
openai.api_key = OPENAI_KEY

app = Flask(__name__)

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)

@app.route("/token", methods=["GET"])
def publish_speech_service_token():
    url = f"https://{SPEECH_SERVICE_REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = { "Ocp-Apim-Subscription-Key": SPEECH_SERVICE_KEY }
    resp = requests.post(url, headers=headers)
    return jsonify({ "token": resp.text, "region": SPEECH_SERVICE_REGION }), 200

@app.route("/completion", methods=["POST"])
def generate_completion():
    prompt = request.json["prompt"]
    resp = openai.ChatCompletion.create(
        engine=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": OPENAI_SYSTEM_MESSAGE},
            {"role": "user", "content": prompt}
        ],
        max_tokens=OPENAI_MAX_TOKEN,
        temperature=OPENAI_TEMPERATURE
    )
    completion = resp["choices"][0]["message"]["content"]
    return jsonify({ "completion": completion }), 200

if __name__ == "__main__":
    app.run()