import argparse
import yaml
from agent.runtime import AgentRuntime
from agent.tools import svn_diff_tool
from agent.prompts import AUDIT_PROMPT
from models.anthropic_client import ClaudeClient


def load_config(path: str = "config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    parser = argparse.ArgumentParser(description="SVN Code Review CLI (cr-cli)")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--svn-path", required=True, help="SVN 工作副本路径或文件路径")
    parser.add_argument("--revision", type=int, required=True, help="SVN 版本号")
    args = parser.parse_args()

    cfg = load_config(args.config)
    model_cfg = cfg["model"]

    model = ClaudeClient(
        model_name=model_cfg["name"],
        api_key_env=model_cfg.get("api_key_env", "ANTHROPIC_API_KEY"),
    )

    tools = [svn_diff_tool()]
    agent = AgentRuntime(model, tools)

    diff_text = agent.get_svn_diff(args.revision, args.svn_path)
    result = agent.run_audit(AUDIT_PROMPT, diff_text)

    print(result)


if __name__ == "__main__":
    main()
