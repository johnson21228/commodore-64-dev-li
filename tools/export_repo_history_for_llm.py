#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime
import hashlib
import subprocess

out_dir = Path("outputs/history")
out_dir.mkdir(parents=True, exist_ok=True)

def run(cmd):
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT).strip()
    except Exception as e:
        return f"[command failed: {' '.join(cmd)}]\n{e}"

status = run(["git", "status", "--short"])
log = run(["git", "log", "--oneline", "--decorate", "--max-count=40"])
branch = run(["git", "branch", "--show-current"])
files = run(["git", "ls-files"])

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
digest = hashlib.sha1((status + log + files).encode("utf-8")).hexdigest()[:7]
out = out_dir / f"repo_history_for_llm_{stamp}_{digest}.md"

out.write_text(f"""# Repository History for LLM

Generated: {stamp}
Branch: {branch or '[unknown]'}

## Recent commits

```text
{log or '[no git log available]'}
```

## Working tree status

```text
{status or '[clean]'}
```

## Tracked files

```text
{files or '[no tracked files available]'}
```
""", encoding="utf-8")
print(f"Wrote {out}")
