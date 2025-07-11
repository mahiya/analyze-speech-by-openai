import os
import json
from openai import OpenAI


class AzureOpenAIClient:

    def __init__(
        self,
        endpoint: str = None,
        api_key: str = None,
    ):
        endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
        if endpoint.endswith("/"):
            endpoint = endpoint[:-1]
        self.client = OpenAI(
            base_url=f"{endpoint}/openai/v1/",
            api_key=api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            default_query={"api-version": "preview"},
        )
        self.max_tokens = int(os.environ.get("AZURE_OPENAI_MAX_TOKENS", 32768))
        self.max_reasoning_tokens = int(os.environ.get("AZURE_OPENAI_REASONING_MAX_TOKENS", 100000))

    def get_response(self, system_message: str, user_message: str, model: str = "gpt-4.1", json_mode: bool = False):
        reasoning_model = model.startswith("o") or model.startswith("codex")
        resp = self.client.responses.create(
            model=model,
            input=[{"role": "system", "content": system_message}, {"role": "user", "content": user_message}],
            temperature=None if reasoning_model else 0.0,
            text={"format": {"type": "json_object"}} if json_mode else None,
            max_output_tokens=self.max_reasoning_tokens if reasoning_model else self.max_tokens,
        )
        content = resp.output[-1].content[0].text
        return json.loads(content) if json_mode else content
