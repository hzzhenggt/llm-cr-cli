import subprocess
from dataclasses import dataclass
from typing import Callable, Dict, Any


@dataclass
class Tool:
    name: str
    description: str
    func: Callable[[Dict[str, Any]], str]


def svn_diff_tool():
    def run(args: Dict[str, Any]) -> str:
        revision = int(args["revision"])
        path = args["path"]
        cmd = ["svn", "diff", "-r", f"{revision-1}:{revision}", path]
        diff = subprocess.check_output(cmd, encoding="utf-8", errors="ignore")
        return diff

    return Tool(
        name="svn_diff",
        description="读取指定 SVN 版本的 diff",
        func=run,
    )
