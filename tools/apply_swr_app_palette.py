from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
MARKER_START = "/* SWR APP PALETTE START */"
MARKER_END = "/* SWR APP PALETTE END */"

REPLACEMENTS = {
    "#061019": "#070704",
    "#0d1925": "#11100b",
    "#122337": "#19160d",
    "#29435e": "#715d24",
    "#eef7ff": "#f7f1df",
    "#9fb4c9": "#b6aa85",
    "#65d9ef": "#d5b44a",
    "#ffd66f": "#e4c85e",
    "#76caff": "#d5b44a",
    "#152b45": "#2a230e",
    "#08131f": "#0b0a06",
    "#050a11": "#030302",
    "#22384f": "#715d24",
    "#3a5d7b": "#8a702b",
    "#10263a": "#1b170b",
    "#dcf6ff": "#fff6d3",
    "#213850": "#5e4c1d",
    "#09131e": "#080704",
    "#c7d9eb": "#e6d9af",
    "#304c68": "#765f24",
    "#3a5872": "#765f24",
    "#101f2e": "#17140a",
    "#d9ebf9": "#f2e8cc",
    "#3b5872": "#765f24",
    "#0b1723": "#100f09",
    "#a8bfd3": "#d2c49f",
    "#3b5d78": "#7a6327",
    "#102437": "#1b170b",
    "#d9f2ff": "#f8efcf",
    "#527b9c": "#9d7e2e",
    "#d2efff": "#f3e8c2",
    "#263f59": "#604d1d",
    "#35516b": "#715b22",
    "#b8d2e7": "#decfa9",
    "#dcefff": "#f8efd2",
    "#385a76": "#765f24",
    "#112a3e": "#1d180a",
    "#d9efff": "#f4e8c6",
    "#29465f": "#65511e",
    "#091722": "#0e0d07",
    "#e6f4ff": "#fff4cf",
    "#3b5b75": "#7a6327",
    "#102233": "#17140a",
    "#33536f": "#715b22",
    "#0b1a28": "#111008",
    "#b9d5ea": "#e2d5b1",
    "#233c55": "#5d4a1b",
    "#c5d8e9": "#e3d6b3",
    "#304b66": "#735c22",
    "#dcecff": "#f1e7c9",
    "#101e2c": "#151208",
    "#5983a7": "#b08e35",
    "#19415a": "#3a2f0e",
    "#6bdaf2": "#e0bd50",
    "rgba(102,217,239,.15)": "rgba(213,180,74,.18)",
    "#aebfd1": "#c9bb96",
    "#304a64": "#705a20",
    "#0f1d2a": "#141107",
    "#e7f2fc": "#f4ead0",
    "#5c85aa": "#b08e35",
    "#66d9ef": "#d5b44a",
    "#193e56": "#392d0d",
    "#3b5671": "#725b22",
    "#111f2d": "#161309",
    "#2a435d": "#65511f",
    "#527b9f": "#a98631",
    "#16364e": "#34290d",
    "#65d4ef": "#d5b44a",
    "#7f95aa": "#9d916f",
    "#294159": "#65511f",
    "#eaf7ff": "#f7f0dc",
    "#4e9fbe": "#b28d32",
    "#173c52": "#34290d",
    "#effcff": "#fff8df",
    "#a9c3d8": "#d8cba6",
    "#34516b": "#715b22",
    "#102033": "#1a160a",
    "#cce7f8": "#f0e4c0",
    "#36516b": "#715b22",
    "#7f96ab": "#9f9370",
    "#23394f": "#594819",
    "#0b1825": "#0f0e09",
    "#2e4a63": "#6f5a22",
    "#eff8ff": "#fff8df",
    "#8fa8bd": "#aa9d79",
    "#c9d9e7": "#ded4b3",
    "#3b5871": "#745e25",
    "rgba(5,11,18,.96)": "rgba(4,4,3,.97)",
}

PALETTE_OVERRIDES = r'''

/* SWR APP PALETTE START */
:root{
  --bg:#070704;--panel:#11100b;--panel2:#19160d;--line:#715d24;
  --text:#f7f1df;--muted:#b6aa85;--accent:#d5b44a;--blue:#d5b44a;
}
body{
  background:radial-gradient(circle at 50% 0,#2a230e 0,#0b0a06 42%,#030302 100%);
}
header{
  background:rgba(4,4,3,.97);border-bottom-color:#715d24;
  box-shadow:0 8px 30px rgba(0,0,0,.38);
}
.panel{
  border-color:#5e4c1d;background:linear-gradient(180deg,#14120b,#080704);
  box-shadow:0 16px 42px rgba(0,0,0,.34);
}
main h2,main h3{color:#e6d9af}
a{color:#e0bd50}
select,input[type="search"],input[list],input[type="text"],input[type="url"],textarea{
  color:#f7f1df;background:#0b0a06;border-color:#765f24;
}
select:focus,input:focus,textarea:focus{border-color:#d5b44a;box-shadow:0 0 0 2px rgba(213,180,74,.12)}
input[type="checkbox"],input[type="radio"]{accent-color:#d5b44a}
button:not(.warn):not(.remove):not(.danger):not([class*="delete"]){
  border-color:#765f24;background:#17140a;color:#f2e8cc;
}
button:not(.warn):not(.remove):not(.danger):not([class*="delete"]):hover{
  border-color:#d5b44a;color:#fff6d3;box-shadow:0 0 0 1px rgba(213,180,74,.12) inset;
}
button.active:not(.warn):not(.remove):not(.danger),
.favorite-btn.active,.macro.active,.player-btn.active,.assign-btn.active{
  border-color:#e0bd50;background:#3a2f0e;color:#fff6d3;
  box-shadow:0 0 0 1px rgba(213,180,74,.18) inset;
}
.stat,.chip,.frequency-badge:not(.primary):not(.frequent):not(.occasional):not(.alert),.scout-summary span{
  border-color:#806827;background:#1b170b;color:#f3e8c2;
}
.subpanel,.note,.global-result,.empty-state,.mapping-bar,.selected-card,
.scout-report,.scout-matchup,.tendency-builder,.tendency-board,
.handoff-input,.handoff-output,.scout-concept-note,.tendency-context{
  border-color:#5e4c1d;background:#0d0c07;
}
::selection{background:#8a702b;color:#fff8df}
*{scrollbar-color:#715d24 #080704}
/* SWR APP PALETTE END */
'''


def script_region(document: str) -> str:
    start = document.find("<script")
    end = document.rfind("</script>")
    if start < 0 or end < 0:
        raise RuntimeError("Could not locate application script region")
    return document[start : end + len("</script>")]


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    original = INDEX.read_text(encoding="utf-8")
    if MARKER_START in original:
        print("SWR app palette already applied; nothing to do")
        return

    original_ids = re.findall(r'\bid="([^"]+)"', original)
    original_script_hash = sha256(script_region(original))

    style_end = original.find("</style>")
    if style_end < 0:
        raise RuntimeError("Could not locate style block")

    style = original[:style_end]
    remainder = original[style_end:]
    for old, new in REPLACEMENTS.items():
        style = re.sub(re.escape(old), new, style, flags=re.IGNORECASE)

    updated = style + PALETTE_OVERRIDES + remainder

    if re.findall(r'\bid="([^"]+)"', updated) != original_ids:
        raise RuntimeError("Existing application IDs changed during palette update")
    if sha256(script_region(updated)) != original_script_hash:
        raise RuntimeError("Application JavaScript changed during palette update")
    if updated.count(MARKER_START) != 1 or updated.count(MARKER_END) != 1:
        raise RuntimeError("Palette marker count is invalid")
    if "#061019" in updated[:updated.find("</style>")].lower():
        raise RuntimeError("Legacy primary blue background remains")
    if "#65d9ef" in updated[:updated.find("</style>")].lower():
        raise RuntimeError("Legacy cyan accent remains")
    if "#315d43" not in updated or "#123e2a" not in updated:
        raise RuntimeError("Football field colors changed unexpectedly")
    if "#ff96d7" not in updated:
        raise RuntimeError("Route visualization colors changed unexpectedly")
    if "width:min(1200px,calc(100% - 28px));max-width:1200px" not in updated:
        raise RuntimeError("Approved banner width cap changed")
    palette = updated[updated.index(MARKER_START):updated.index(MARKER_END)]
    if "position:fixed" in palette.lower() or "overflow-y" in palette.lower() or "<iframe" in updated.lower():
        raise RuntimeError("Prohibited overlap or nested-scroll rule detected")

    INDEX.write_text(updated, encoding="utf-8")
    print("Saturday War Room black/gold/white app palette applied successfully")


if __name__ == "__main__":
    main()
