from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")

old = "const CHATGPT_HANDOFF_PROMPT=`You are acting as a defensive football gameplan analyst for College Football 27. Use the attached or pasted Opponent Film Analysis Packet."
new = "const CHATGPT_HANDOFF_PROMPT=`Analyze the full packet and independently review the included public YouTube or Twitch video link. Do not limit your analysis to the transcript or written notes. Use the actual video for your own visual football observations when the video is accessible.\n\nYou are acting as a defensive football gameplan analyst for College Football 27. Use the attached or pasted Opponent Film Analysis Packet."

count = text.count(old)
if count != 1:
    raise SystemExit(f"Expected one ChatGPT handoff prompt anchor, found {count}")

text = text.replace(old, new, 1)
required = [
    "Analyze the full packet and independently review the included public YouTube or Twitch video link.",
    "Do not limit your analysis to the transcript or written notes.",
    "Use the actual video for your own visual football observations when the video is accessible.",
    "FILM ACCESS RULES:",
    "function buildChatGptPacket()",
]
for marker in required:
    if text.count(marker) != 1:
        raise SystemExit(f"Expected exactly one marker after patch: {marker}")

script = re.search(r"<script>(.*)</script>", text, re.S)
if not script:
    raise SystemExit("Could not extract application JavaScript")
Path("/tmp/cfb27-video-instruction.js").write_text(script.group(1), encoding="utf-8")
path.write_text(text, encoding="utf-8")
print("Stronger link-first video analysis instruction added.")
