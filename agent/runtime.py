from typing import List, Dict, Any
from .tools import Tool


class AgentRuntime:
    def __init__(self, model_client, tools: List[Tool]):
        self.model = model_client
        self.tools = {t.name: t for t in tools}

    def get_svn_diff(self, revision: int, path: str) -> str:
        tool = self.tools["svn_diff"]
        return tool.func({"revision": revision, "path": path})

    def run_audit(self, prompt_template: str, diff_text: str) -> str:
        prompt = prompt_template.replace("{{DIFF}}", diff_text)
        messages = [
            {"role": "user", "content": prompt}
        ]
        return self.model.chat(messages)
