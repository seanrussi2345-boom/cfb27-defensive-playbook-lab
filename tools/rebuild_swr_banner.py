from __future__ import annotations

import base64
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / ".banner-replacement"
ASSET = ROOT / "assets" / "swr-banner.webp"
INDEX = ROOT / "index.html"
EXPECTED_SHA256 = "e25b3c726e179e2fbf9b2683b9a236844407063ca7141cd6160af733a9462d58"
EXPECTED_SIZE = 63198


def webp_dimensions(data: bytes) -> tuple[int, int]:
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise RuntimeError("Rebuilt asset is not a WebP file")
    marker = data[12:16]
    if marker == b"VP8 ":
        start = 20
        if data[start + 3:start + 6] != b"\x9d\x01\x2a":
            raise RuntimeError("Invalid VP8 frame header")
        width = int.from_bytes(data[start + 6:start + 8], "little") & 0x3FFF
        height = int.from_bytes(data[start + 8:start + 10], "little") & 0x3FFF
        return width, height
    if marker == b"VP8X":
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
        return width, height
    raise RuntimeError(f"Unsupported WebP chunk: {marker!r}")


def main() -> None:
    names = ["part_aa1.txt", "part_aa2.txt", "part_ab.txt", "part_ac.txt", "part_ad.txt"]
    encoded = "".join((PARTS / name).read_text(encoding="ascii").strip() for name in names)
    data = base64.b64decode(encoded, validate=True)
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != EXPECTED_SIZE:
        raise RuntimeError(f"Wrong banner size: {len(data)} bytes")
    if digest != EXPECTED_SHA256:
        raise RuntimeError(f"Wrong banner checksum: {digest}")
    dimensions = webp_dimensions(data)
    if dimensions != (1200, 400):
        raise RuntimeError(f"Wrong banner dimensions: {dimensions}")

    ASSET.write_bytes(data)

    html = INDEX.read_text(encoding="utf-8")
    old = "width:min(1760px,calc(100% - 28px));max-width:100%;min-width:0;"
    new = "width:min(1200px,calc(100% - 28px));max-width:1200px;min-width:0;"
    if old in html:
        html = html.replace(old, new, 1)
    elif new not in html:
        raise RuntimeError("Could not locate the banner width rule")
    if "<iframe" in html.lower():
        raise RuntimeError("Iframe detected")
    branding = html[html.index("/* SWR BRANDING START */"):html.index("/* SWR BRANDING END */")]
    if "position:fixed" in branding.lower():
        raise RuntimeError("Fixed branding element detected")
    INDEX.write_text(html, encoding="utf-8")

    print(f"Banner verified: {dimensions[0]}x{dimensions[1]}, {len(data)} bytes, {digest}")


if __name__ == "__main__":
    main()
