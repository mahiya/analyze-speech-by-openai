from flask import Flask, request
import os
import requests
from dotenv import load_dotenv
from utils.openai import AzureOpenAIClient

# .env ファイルから環境変数を読み込む
load_dotenv()
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-nano")
SPEECH_SERVICE_REGION = os.environ.get("SPEECH_SERVICE_REGION")
SPEECH_SERVICE_KEY = os.environ.get("SPEECH_SERVICE_KEY")

# Azure OpenAI Service で使用するシステムメッセージの定義
SYSTEM_MESSAGE = """
リアルタイムで音声を文字起こしした内容を箇条書きで要約してください
要約した内容を以下の JSON 形式で返してください：
{
    "summary": str // 要約した内容
}
"""

# Azure OpenAI Client のインスタンスを作成
openai_client = AzureOpenAIClient()

# Flask アプリケーションのインスタンスを作成
app = Flask(__name__)


# 静的ファイルのルーティング
@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)


# Azure Speech Service の一時利用トークンを発行する Web API
@app.route("/api/token", methods=["GET"])
def publish_speech_service_token():
    url = f"https://{SPEECH_SERVICE_REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {"Ocp-Apim-Subscription-Key": SPEECH_SERVICE_KEY}
    resp = requests.post(url, headers=headers)
    return {"token": resp.text, "region": SPEECH_SERVICE_REGION}


# 入力した音声の文字書き起こし内容を要約する Web API
@app.route("/api/modify", methods=["POST"])
def modify_text_api():
    return openai_client.get_response(
        model=AZURE_OPENAI_DEPLOYMENT,
        system_message=SYSTEM_MESSAGE,
        user_message=request.json["text"],
        json_mode=True,
    )


# Flask アプリケーションを起動する
if __name__ == "__main__":
    app.run()
