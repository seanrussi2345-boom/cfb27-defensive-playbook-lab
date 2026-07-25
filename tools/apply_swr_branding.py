from __future__ import annotations

import base64
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH_DIR = ROOT / ".swr-branding-patch"
INDEX = ROOT / "index.html"
ASSETS = ROOT / "assets"

BANNER_PARTS = [PATCH_DIR / f"banner_{i:02d}.txt" for i in range(6)]
LOGO_PARTS = [PATCH_DIR / f"logo_{i:02d}.txt" for i in range(2)]

BRANDING_CSS = r'''

/* SWR BRANDING START */
html{scroll-padding-top:92px}
body{overflow-x:hidden}
.swr-header-brand{display:flex;align-items:center;gap:11px;min-width:0}
.swr-header-logo{
  display:block;width:46px;height:46px;flex:0 0 46px;object-fit:cover;border-radius:50%;
  border:2px solid #c7a33a;background:#05080c;box-shadow:0 0 0 2px rgba(0,0,0,.45),0 7px 20px rgba(0,0,0,.42)
}
.swr-header-copy{min-width:0}
.swr-brand-hero{
  position:relative;z-index:1;width:min(1760px,calc(100% - 28px));max-width:100%;min-width:0;
  margin:14px auto 0;overflow:hidden;border:1px solid #715d24;border-radius:16px;background:#05080c;
  box-shadow:0 16px 42px rgba(0,0,0,.32)
}
.swr-brand-banner{
  display:block;width:100%;max-width:100%;height:auto;aspect-ratio:3/1;
  object-fit:cover;object-position:center;pointer-events:none;user-select:none
}
@media(max-width:850px){
  html{scroll-padding-top:12px}
  .swr-brand-hero{width:calc(100% - 18px);margin-top:9px;border-radius:11px}
  .swr-header-brand{width:100%}
}
@media(max-width:520px){
  .swr-header-logo{width:42px;height:42px;flex-basis:42px}
  .swr-header-copy h1{font-size:17px}
  .swr-header-copy p{font-size:10px;line-height:1.35}
  .swr-brand-hero{border-radius:9px}
}
/* SWR BRANDING END */
'''

HEADER_OLD = '''  <div>
    <h1>Saturday War Room <span style="color:#65d9ef">v5.0</span></h1>
    <p>Wreck your dynasty opponent's offense. Build the answer before kickoff.</p>
  </div>'''

HEADER_NEW = '''  <div class="swr-header-brand">
    <img class="swr-header-logo" src="assets/swr-logo.webp" alt="Saturday War Room logo" width="46" height="46">
    <div class="swr-header-copy">
      <h1>Saturday War Room <span style="color:#65d9ef">v5.0</span></h1>
      <p>Wreck your dynasty opponent's offense. Build the answer before kickoff.</p>
    </div>
  </div>'''

HERO = '''

<!-- SWR BRANDING START -->
<section class="swr-brand-hero" aria-label="Saturday War Room branding">
  <img class="swr-brand-banner" src="assets/swr-banner.webp" alt="Saturday War Room football strategy and gameplanning banner" width="1200" height="400" fetchpriority="high" decoding="async">
</section>
<!-- SWR BRANDING END -->'''

HEAD_LINKS = '''
<link rel="icon" type="image/webp" href="assets/swr-logo.webp">
<link rel="apple-touch-icon" href="assets/swr-logo.webp">
<meta name="theme-color" content="#090a08">'''


def decode_parts(parts: list[Path], destination: Path, expected_size: int) -> None:
    encoded = "".join(part.read_text(encoding="ascii").strip() for part in parts)
    payload = base64.b64decode(encoded, validate=True)
    if len(payload) != expected_size:
        raise RuntimeError(f"Unexpected decoded size for {destination}: {len(payload)}")
    if not (payload.startswith(b"RIFF") and payload[8:12] == b"WEBP"):
        raise RuntimeError(f"Decoded asset is not WebP: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)


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
    if "<!-- SWR BRANDING START -->" in original:
        raise RuntimeError("Branding marker already exists; refusing to apply twice")

    original_ids = re.findall(r'\bid="([^"]+)"', original)
    original_script_hash = sha256(script_region(original))

    if HEADER_OLD not in original:
        raise RuntimeError("Expected header block was not found")
    if original.count("</style>") != 1:
        raise RuntimeError("Expected exactly one style block")
    if original.count("</header>") != 1:
        raise RuntimeError("Expected exactly one application header")
    if original.count("</title>") != 1:
        raise RuntimeError("Expected exactly one title element")

    updated = original.replace("</title>", "</title>" + HEAD_LINKS, 1)
    updated = updated.replace("</style>", BRANDING_CSS + "\n</style>", 1)
    updated = updated.replace(HEADER_OLD, HEADER_NEW, 1)
    updated = updated.replace("</header>", "</header>" + HERO, 1)

    updated_ids = re.findall(r'\bid="([^"]+)"', updated)
    if updated_ids != original_ids:
        raise RuntimeError("Existing application IDs changed during branding patch")
    if sha256(script_region(updated)) != original_script_hash:
        raise RuntimeError("Application JavaScript changed during branding patch")
    if updated.index("swr-brand-hero") > updated.index('<main class="app">'):
        raise RuntimeError("Brand banner was not inserted before the application menus")
    if "<iframe" in updated.lower():
        raise RuntimeError("Iframe detected; nested-scroll layouts are not allowed")
    if "position:fixed" in BRANDING_CSS.lower() or "overflow-y" in BRANDING_CSS.lower():
        raise RuntimeError("Branding CSS contains a prohibited fixed or nested vertical-scroll rule")

    decode_parts(BANNER_PARTS, ASSETS / "swr-banner.webp", 56678)
    decode_parts(LOGO_PARTS, ASSETS / "swr-logo.webp", 14874)
    INDEX.write_text(updated, encoding="utf-8")

    print("Saturday War Room branding applied successfully")
    print(f"index.html bytes: {INDEX.stat().st_size}")
    print(f"banner bytes: {(ASSETS / 'swr-banner.webp').stat().st_size}")
    print(f"logo bytes: {(ASSETS / 'swr-logo.webp').stat().st_size}")


if __name__ == "__main__":
    main()
