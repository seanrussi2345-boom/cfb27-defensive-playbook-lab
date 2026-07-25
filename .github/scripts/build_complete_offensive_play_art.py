from pathlib import Path
import base64
import re
import zlib

INDEX = Path("index.html")
README = Path("README.md")
text = INDEX.read_text(encoding="utf-8")

BLOCK = zlib.decompress(base64.b64decode("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")).decode("utf-8")

pattern = r'function scoutSetTargets\(set,strength\)\{.*?\n\}\nfunction scoutDefenseCoords\(ids\)\{'
text, count = re.subn(pattern, BLOCK + "\nfunction scoutDefenseCoords(ids){", text, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f"Expected one offensive concept renderer block, found {count}")

old_description = 'el("scoutConceptDescription").innerHTML=`<strong>${concept.category}: ${concept.name}</strong><br>${concept.description}`;'
new_description = 'el("scoutConceptDescription").innerHTML=`<strong>${concept.category}: ${concept.name}</strong><br>${concept.description}<br><span style="color:#79dced">Complete 11-player responsibility art: routes, run tracks, reads, protection, and blocking.</span>`;'
if text.count(old_description) != 1:
    raise SystemExit("Scout concept description anchor missing")
text = text.replace(old_description, new_description, 1)

release_marker = '<div class="release-list">'
release_item = '<div class="release-list">\n            <article class="release-item"><strong>Complete offensive play art</strong><span>Every offensive player now receives one visible responsibility across every offensive set, concept, and passing-strength direction: route, run track, quarterback action/read, pass protection, lead block, screen block, or stalk block.</span></article>'
if text.count(release_marker) != 1:
    raise SystemExit("Release-list anchor missing")
text = text.replace(release_marker, release_item, 1)

INDEX.write_text(text, encoding="utf-8")

readme = README.read_text(encoding="utf-8")
marker = '- Base Offensive Concept layer with grouped pass, run, option, screen, and RPO selections; route/run visualization; concept-specific defensive stress alerts; and concept metadata preserved in saved scout matchups and Weekly Gameplan calls\n'
feature = '- Complete 11-player offensive responsibility art across every offensive set, concept, and left/right strength combination, including complementary routes, quarterback actions, pass protection, run blocking, lead blocks, screen blocks, and stalk blocks\n'
if feature not in readme:
    if marker not in readme:
        raise SystemExit("README offensive-concept marker missing")
    readme = readme.replace(marker, marker + feature, 1)
README.write_text(readme, encoding="utf-8")

required = [
    'function scoutConceptPlan(set,conceptId,strength)',
    'function offensiveConceptCoverageReport()',
    'Complete 11-player responsibility art',
    'plan.paths.forEach(path=>scoutPath',
]
for item in required:
    if text.count(item) != 1:
        raise SystemExit(f"Expected exactly one integration marker: {item}")

script = re.search(r'<script>(.*)</script>', text, re.S)
if not script:
    raise SystemExit("Could not extract complete application JavaScript")
Path('/tmp/cfb27-complete-offensive-art.js').write_text(script.group(1), encoding='utf-8')

coverage = re.search(r'(const OFFENSIVE_SCOUT_SETS=.*?)(?=\nfunction scoutDefenseCoords\(ids\))', text, re.S)
if not coverage:
    raise SystemExit("Could not extract offensive concept coverage section")
coverage_test = coverage.group(1) + '''\nconst coverageReport=offensiveConceptCoverageReport();\nconsole.log(`Validated ${coverageReport.tested} offensive set/concept/strength combinations.`);\nif(coverageReport.failures.length){console.error(JSON.stringify(coverageReport.failures,null,2));process.exit(1);}\n'''
Path('/tmp/cfb27-offensive-coverage.js').write_text(coverage_test, encoding='utf-8')
print('Complete offensive play-art patch validation passed.')
