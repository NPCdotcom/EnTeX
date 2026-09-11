import re, sys
from pathlib import Path
root = Path(r"C:\Users\npcdo\.agents\skills")
# descriptions passed via a sidecar file
import json
descs = json.loads(Path(r"C:\Users\npcdo\.agents\memory\history\desc-map.json").read_text(encoding="utf-8"))
for name, desc in descs.items():
    skill = root / name / "SKILL.md"
    if not skill.is_file():
        print("MISSING", name)
        continue
    text = skill.read_text(encoding="utf-8")
    new, n = re.subn(r"(?m)^description:\s*.+$", f"description: {desc}", text, count=1)
    if n:
        skill.write_text(new, encoding="utf-8")
        print("OK", name)
    else:
        print("NO_DESC", name)
