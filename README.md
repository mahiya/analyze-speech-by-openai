# リアルタイム音声認識＋要約のサンプルアプリ

## 必要なもの
- Azure OpenAI Service のアカウント ([参考](https://learn.microsoft.com/ja-jp/azure/ai-foundry/openai/how-to/create-resource?pivots=web-portal))
- Azure Speech Service のアカウント ([参考](https://learn.microsoft.com/ja-jp/azure/ai-services/multi-service-resource?pivots=azportal))
- Python 実行環境 ([参考](https://www.python.org/downloads/), 3.11.9 で動作確認済み)

## ローカル環境の設定

[.env](./.env) の下記プロパティを設定します。
 - ```AZURE_OPENAI_ENDPOINT```: 使用する Azure OpenAI Service のエンドポイント
 - ```AZURE_OPENAI_API_KEY```: Azure OpenAI Service アカウントの認証キー
 - ```AZURE_OPENAI_DEPLOYMENT```: Azure OpenAI Service アカウントのモデルのデプロイメント名
 - ```SPEECH_SERVICE_REGION```: Azure Speech Service アカウントのリージョン名
 - ```SPEECH_SERVICE_KEY```: Azure Speech Service アカウントの認証キー

## ローカル環境での実行方法

以下のコマンドを実行して Python モジュールをインストールします。
```bash
pip install -r requirements.txt
```

以下の通りに [app.py](./app.py) を実行して、Web アプリケーションを起動します。
```bash
python app.py
```

```http://127.0.0.1:5000``` を Web ブラウザで開くことで、アプリケーションを利用することができます。

![画面イメージ](.images/screenshot.png)

