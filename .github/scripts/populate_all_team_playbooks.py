import json
import re
import time
import unicodedata
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

TEAM_SCHEMES = json.loads(r'''{"3-3-5":["Arizona","Georgia State","Marshall","Mississippi State","West Virginia"],"3-3-5 Man":["Sam Houston"],"3-3-5 Man Pressure":["Louisiana Tech"],"3-3-5 Shell":["Baylor","Kennesaw State","New Mexico State","North Texas","Tulsa"],"3-3-5 Three High":["Delaware","East Carolina","Troy","UL Monroe","UTEP"],"3-3-5 Tite":["Auburn","Colorado State","Florida Atlantic","Georgia","Missouri State","South Florida","Texas","Tulane"],"3-3-5 Zone":["Florida State","TCU"],"3-3-5 Zone Pressure":["Arkansas","Georgia Tech","Houston","Jacksonville State","James Madison","Navy","Southern Mississippi","Western Kentucky"],"3-4":["Georgia Southern"],"3-4 Man":["Illinois","Middle Tennessee State","Penn State"],"3-4 Man Pressure":["Hawaii","Maryland","Rice","UAB","Washington"],"3-4 Multiple":["California","Florida","North Carolina"],"3-4 Shell":["NC State","Oregon","Texas Tech"],"3-4 Zone":["Air Force","Alabama","Central Michigan","Kansas","Liberty","Oregon State","Temple"],"3-4 Zone Pressure":[],"4-2-5":["Arkansas State","Ole Miss","San Diego State","Syracuse","Virginia"],"4-2-5 Man":["Appalachian State","Boise State","Bowling Green","Duke","Massachusetts","South Carolina","Wyoming"],"4-2-5 Man Pressure":["Buffalo","Colorado","Memphis","Minnesota","Nebraska","Ohio State","Oklahoma","SMU","UCLA","UNLV"],"4-2-5 Shell":["Coastal Carolina","Northern Illinois","Northwestern","Rutgers","Tennessee","Toledo","USC"],"4-2-5 Zone":["Charlotte","Fresno State","Iowa State","Louisville","Missouri","Sacramento State"],"4-2-5 Zone Pressure":["Arizona State","Kansas State","Kentucky","Miami (FL)","Michigan State","Ohio","South Alabama","Texas A&M","Vanderbilt","Wake Forest","Western Michigan"],"4-3":["Boston College","Louisiana","North Dakota State"],"4-3 Man":["Eastern Michigan"],"4-3 Man Pressure":["BYU","Michigan","Utah"],"4-3 Multiple":["San Jose State","UCF","Wisconsin"],"4-3 Press Quarters":["Pittsburgh","UConn"],"4-3 Shell":["Iowa"],"4-3 Zone":["Miami (OH)","Stanford","New Mexico"],"4-3 Zone Pressure":["Indiana"],"3-2-6":["Old Dominion"],"Multiple":["Ball State","Clemson","Florida International","Kent State","LSU","Nevada","Notre Dame","Oklahoma State","Purdue","Washington State","Akron","Army","Cincinnati","Texas State","Utah State","UTSA","Virginia Tech"]}''')
EXPECTED_SCHEMES = set(TEAM_SCHEMES) | {"3-4 Zone Pressure"}

all_teams = [team for teams in TEAM_SCHEMES.values() for team in teams]
if len(all_teams) != 138:
    raise SystemExit(f"Expected 138 teams, found {len(all_teams)}.")
if len(set(all_teams)) != 138:
    duplicates = sorted(team for team, count in __import__("collections").Counter(all_teams).items() if count > 1)
    raise SystemExit(f"Duplicate team assignments: {duplicates}")
if len(EXPECTED_SCHEMES) != 31:
    raise SystemExit(f"Expected 31 defensive playbooks, found {len(EXPECTED_SCHEMES)}.")

app_path = Path("index.html")
text = app_path.read_text(encoding="utf-8")
db_match = re.search(r"const PLAY_DB = (\{.*?\});\n\nconst TEAM_PLAYBOOK_SCHEMES=", text, re.S)
if not db_match:
    raise SystemExit("Could not locate the app's master PLAY_DB.")
play_db = json.loads(db_match.group(1))

def clean(value):
    return re.sub(r"\s+", " ", value or "").strip()

def normalized(value):
    value = unicodedata.normalize("NFKD", clean(value)).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^A-Z0-9]+", "", value.upper())

def canonical_path(url):
    path = urlparse(url).path.rstrip("/")
    if path.startswith("/27/"):
        path = path[3:]
    return path

session = requests.Session()
retry = Retry(
    total=5,
    connect=5,
    read=5,
    backoff_factor=0.7,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=("GET",),
)
session.mount("https://", HTTPAdapter(max_retries=retry))
session.headers.update({
    "User-Agent": "Mozilla/5.0 (compatible; CFB27-Playbook-Lab/1.0; +https://github.com/seanrussi2345-boom/cfb27-defensive-playbook-lab)",
    "Accept-Language": "en-US,en;q=0.9",
})

def fetch(url):
    response = session.get(url, timeout=30)
    response.raise_for_status()
    time.sleep(0.08)
    return response

def direct_child_links(soup, base_url):
    base_path = canonical_path(base_url)
    found = {}
    for anchor in soup.select("a[href]"):
        absolute = urljoin(base_url, anchor.get("href"))
        child_path = canonical_path(absolute)
        if not child_path.startswith(base_path + "/"):
            continue
        if child_path.count("/") != base_path.count("/") + 1:
            continue
        label = clean(anchor.get_text(" ", strip=True))
        if label:
            found[absolute] = label
    return found

article_url = "https://cfb.fan/news/cut-27-team-defense-playbook-schemes/"
article = fetch(article_url)
article_soup = BeautifulSoup(article.text, "html.parser")
scheme_urls = {}
for anchor in article_soup.select("a[href]"):
    absolute = urljoin(article.url, anchor.get("href"))
    path = canonical_path(absolute)
    if re.fullmatch(r"/playbooks/[^/]+-def", path):
        scheme_urls[absolute] = None

if len(scheme_urls) != 31:
    raise SystemExit(f"Expected 31 playbook links from CFB.FAN, found {len(scheme_urls)}.")

formation_exact = {name: name for name in play_db}
formation_norm = {}
for name in play_db:
    formation_norm.setdefault(normalized(name), []).append(name)

def resolve_formation(source_name):
    if source_name in formation_exact:
        return source_name
    matches = formation_norm.get(normalized(source_name), [])
    if len(matches) == 1:
        return matches[0]
    raise ValueError(f"Formation does not resolve uniquely: {source_name!r} -> {matches}")

def resolve_play(formation, source_name):
    plays = play_db[formation]
    if source_name in plays:
        return source_name
    by_norm = {}
    for play in plays:
        by_norm.setdefault(normalized(play), []).append(play)
    matches = by_norm.get(normalized(source_name), [])
    if len(matches) == 1:
        return matches[0]
    raise ValueError(f"Play does not resolve uniquely: {formation} — {source_name!r} -> {matches}")

scheme_data = {}
scrape_errors = []
for scheme_url in sorted(scheme_urls):
    response = fetch(scheme_url)
    soup = BeautifulSoup(response.text, "html.parser")
    heading = soup.find("h1")
    if not heading:
        scrape_errors.append(f"No scheme heading: {response.url}")
        continue
    scheme_name = clean(heading.get_text(" ", strip=True))
    if scheme_name not in EXPECTED_SCHEMES:
        scrape_errors.append(f"Unexpected scheme name {scheme_name!r}: {response.url}")
        continue

    formation_links = direct_child_links(soup, response.url)
    formations = {}
    for formation_url in sorted(formation_links):
        formation_response = fetch(formation_url)
        formation_soup = BeautifulSoup(formation_response.text, "html.parser")
        formation_heading = formation_soup.find("h1")
        if not formation_heading:
            scrape_errors.append(f"No formation heading: {formation_response.url}")
            continue
        source_formation = clean(formation_heading.get_text(" ", strip=True))
        try:
            formation = resolve_formation(source_formation)
        except ValueError as exc:
            scrape_errors.append(str(exc))
            continue

        play_links = direct_child_links(formation_soup, formation_response.url)
        resolved_plays = []
        for _, source_play in play_links.items():
            try:
                resolved_plays.append(resolve_play(formation, source_play))
            except ValueError as exc:
                scrape_errors.append(str(exc))
        resolved_plays = list(dict.fromkeys(resolved_plays))
        if not resolved_plays:
            scrape_errors.append(f"No plays resolved: {scheme_name} — {formation}")
            continue
        formations[formation] = resolved_plays

    if not formations:
        scrape_errors.append(f"No formations resolved: {scheme_name}")
        continue
    scheme_data[scheme_name] = {
        "name": scheme_name,
        "formations": formations,
    }
    print(f"{scheme_name}: {len(formations)} formations, {sum(len(v) for v in formations.values())} plays")

if scrape_errors:
    raise SystemExit("Scrape validation failed:\n" + "\n".join(scrape_errors[:100]))
if set(scheme_data) != EXPECTED_SCHEMES:
    missing = sorted(EXPECTED_SCHEMES - set(scheme_data))
    extra = sorted(set(scheme_data) - EXPECTED_SCHEMES)
    raise SystemExit(f"Scheme mismatch. Missing={missing}; Extra={extra}")

for scheme_name, book in scheme_data.items():
    for formation, plays in book["formations"].items():
        if formation not in play_db:
            raise SystemExit(f"Missing master formation: {scheme_name} — {formation}")
        invalid = [play for play in plays if play not in play_db[formation]]
        if invalid:
            raise SystemExit(f"Missing master plays: {scheme_name} — {formation}: {invalid}")

display_aliases = {
    "California": "Cal",
    "Florida International": "FIU",
    "Hawaii": "Hawai'i",
    "Massachusetts": "UMass",
    "Sam Houston": "Sam Houston State",
    "South Florida": "USF",
    "Southern Mississippi": "Southern Miss",
}
scheme_aliases = {"Multiple": "Multiple D"}

def team_id(name):
    value = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_").upper()
    return value

team_records = []
ids = set()
for scheme_name, teams in TEAM_SCHEMES.items():
    for team in teams:
        identifier = team_id(team)
        if identifier in ids:
            raise SystemExit(f"Duplicate generated team id: {identifier}")
        ids.add(identifier)
        team_records.append({
            "id": identifier,
            "name": display_aliases.get(team, team),
            "scheme": scheme_aliases.get(scheme_name, scheme_name),
            "schemeKey": scheme_name,
        })
team_records.sort(key=lambda record: record["name"])

schemes_json = json.dumps(scheme_data, separators=(",", ":"), ensure_ascii=False)
scheme_block = "const TEAM_PLAYBOOK_SCHEMES=" + schemes_json + ";\n"
team_lines = ["const TEAM_PLAYBOOKS={"]
for index, record in enumerate(team_records):
    comma = "," if index < len(team_records) - 1 else ""
    team_lines.append(
        "  "
        + json.dumps(record["id"])
        + ":{name:"
        + json.dumps(record["name"], ensure_ascii=False)
        + ",scheme:"
        + json.dumps(record["scheme"], ensure_ascii=False)
        + ",formations:TEAM_PLAYBOOK_SCHEMES["
        + json.dumps(record["schemeKey"])
        + "].formations}"
        + comma
    )
team_lines.append("};")
generated = scheme_block + "\n".join(team_lines) + "\n\n"

constants_pattern = re.compile(
    r"const TEAM_PLAYBOOK_SCHEMES=.*?\nconst FAMILY_ORDER=\[",
    re.S,
)
if len(constants_pattern.findall(text)) != 1:
    raise SystemExit("Could not uniquely locate existing team-playbook constants.")
text = constants_pattern.sub(generated + "const FAMILY_ORDER=[", text, count=1)

text = text.replace(
    "Select Florida State or TCU to load its verified 3-3-5 Zone defensive playbook.",
    "Select any team to load its CFB 27 defensive playbook.",
    1,
)

app_path.write_text(text, encoding="utf-8")

readme_path = Path("README.md")
readme = readme_path.read_text(encoding="utf-8")
readme = re.sub(
    r"- Team Playbook view with verified Florida State and TCU 3-3-5 Zone books \(12 formations, 162 plays\), referencing the existing master play database",
    "- Team Playbook view for all 138 teams across all 31 defensive books, with exact formation/play membership referencing the existing master play database",
    readme,
    count=1,
)
if "all 138 teams across all 31 defensive books" not in readme:
    raise SystemExit("README team-playbook description was not updated.")
readme_path.write_text(readme, encoding="utf-8")

audit = {
    "teams": len(team_records),
    "schemes": len(scheme_data),
    "activeSchemes": len({record["schemeKey"] for record in team_records}),
    "schemeFormationMemberships": sum(len(book["formations"]) for book in scheme_data.values()),
    "schemePlayMemberships": sum(
        len(plays)
        for book in scheme_data.values()
        for plays in book["formations"].values()
    ),
}
Path("team-playbook-audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
print(json.dumps(audit, indent=2))

text = Path("index.html").read_text(encoding="utf-8")
required = [
    'value="TEAM">Team Playbook',
    'id="teamPlaybook"',
    'Select any team to load its CFB 27 defensive playbook.',
    'const TEAM_PLAYBOOK_SCHEMES=',
    'const TEAM_PLAYBOOKS={',
    'function teamPlaybookTotals',
]
missing = [value for value in required if value not in text]
if missing:
    raise SystemExit(f"Missing generated application elements: {missing}")
if text.count('id="libraryView"') != 1:
    raise SystemExit("Library menu was duplicated or removed.")
if text.count('id="teamPlaybook"') != 1:
    raise SystemExit("Team selector was duplicated.")

if audit["teams"] != 138:
    raise SystemExit(f"Expected 138 teams, found {audit['teams']}.")
if audit["schemes"] != 31:
    raise SystemExit(f"Expected 31 schemes, found {audit['schemes']}.")
if audit["activeSchemes"] != 30:
    raise SystemExit(f"Expected 30 regular-mode team schemes, found {audit['activeSchemes']}.")

script_match = re.search(r"<script>(.*)</script>", text, re.S)
if not script_match:
    raise SystemExit("Could not extract application JavaScript.")
Path("/tmp/cfb27-app.js").write_text(script_match.group(1), encoding="utf-8")
print("Full team-playbook validation passed.")
