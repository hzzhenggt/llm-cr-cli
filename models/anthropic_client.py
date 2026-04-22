import os
from typing import List, Dict, Any
import requests


class ClaudeClient:
    def __init__(self, model_name: str, api_key_env: str = "ANTHROPIC_API_KEY"):
        self.model = model_name
        self.api_key = os.environ.get(api_key_env)
        if not self.api_key:
            raise RuntimeError(f"环境变量 {api_key_env} 未设置")

        self.base_url = "https://api.anthropic.com/v1/messages"

    def chat(self, messages: List[Dict[str, Any]]) -> str:
        content = []
        for m in messages:
            content.append({"role": m["role"], "content": m["content"]})

        payload = {
            "model": self.model,
            "max_tokens": 2048,
            "messages": content,
        }

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        resp = requests.post(self.base_url, json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()

        parts = data["content"]
        texts = []
        for p in parts:
            if p.get("type") == "text":
                texts.append(p.get("text", ""))
        return "\n".join(texts)
