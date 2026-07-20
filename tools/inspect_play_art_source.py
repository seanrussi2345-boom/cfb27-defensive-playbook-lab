#!/usr/bin/env python3
"""Inspect CollegeFootball.gg play/formation pages for structured play-art data."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "diagnostics" / "source-audit"
OUT.mkdir(parents=True, exist_ok=True)

URL