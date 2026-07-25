from pathlib import Path
import re

path = Path("index.html")
text = path.read_text(encoding="utf-8")

# Move the complete Season Command Center from above the app into the opponent-prep
# workflow, directly above the Weekly Gameplan Builder.
match = re.search(
    r'\n<section class="season-shell" id="seasonCommandCenter">.*?</section>\n\n(?=<main class="app">)',
    text,
    flags=re.S,
)
if not match:
    raise SystemExit("Could not locate the top-level Season Command Center block")
season_block = match.group(0).strip()
text = text[:match.start()] + "\n" + text[match.end():]

gameplan_marker = '<section class="panel gameplan-panel" id="gameplanPanel">'
if text.count(gameplan_marker) != 1:
    raise SystemExit(f"Expected one Weekly Gameplan marker, found {text.count(gameplan_marker)}")
text = text.replace(gameplan_marker, season_block + "\n\n" + gameplan_marker, 1)

# The Command Center now participates in the main application grid.
old_shell_css = '.season-shell{width:min(1760px,100%);margin:14px auto 0;padding:0 14px}'
new_shell_css = '.season-shell{grid-column:1/-1;width:100%;margin:0;padding:0}'
if text.count(old_shell_css) != 1:
    raise SystemExit("Season shell desktop CSS anchor missing")
text = text.replace(old_shell_css, new_shell_css, 1)
text = text.replace('@media(max-width:760px){.season-shell{padding:0 9px}', '@media(max-width:760px){.season-shell{padding:0}', 1)

# Give the active profile an obvious deletion control in addition to card-level delete.
jump_anchor = '<button class="season-btn" id="jumpSeasonGameplan" type="button">Call Sheet</button>'
delete_button = jump_anchor + '\n        <button class="season-btn remove" id="deleteActiveSeasonProfile" type="button">Delete Active War Room</button>'
if text.count(jump_anchor) != 1:
    raise SystemExit("Active Command Center action anchor missing")
text = text.replace(jump_anchor, delete_button, 1)

# A truly blank workspace must not carry a generic opponent label. That label made a
# deleted final profile meaningful enough to be automatically recreated.
old_blank = '''function blankSeasonWorkspace(opponent="",week=""){
  const teamName=seasonTeamName(opponent)||"Opponent";
  return{
    gameplan:normalizeGameplan({name:`${teamName} Defensive Gameplan`,opponent,week,entries:[],updatedAt:null}),'''
new_blank = '''function blankSeasonWorkspace(opponent="",week=""){
  const teamName=seasonTeamName(opponent)||"",planName=teamName?`${teamName} Defensive Gameplan`:"Saturday War Room Weekly Gameplan";
  return{
    gameplan:normalizeGameplan({name:planName,opponent,week,entries:[],updatedAt:null}),'''
if text.count(old_blank) != 1:
    raise SystemExit("Blank Season workspace anchor missing")
text = text.replace(old_blank, new_blank, 1)

# Replace the deletion routine so the active workspace is cleared synchronously,
# the next valid profile is loaded when available, and the user is returned to the
# Command Center after the profile is gone.
delete_pattern = r'function deleteSeasonProfile\(id\)\{.*?\n\}'
new_delete = '''function deleteSeasonProfile(id){
  let season=getSeasonCommandCenter(),profile=season.profiles.find(item=>item.id===id);if(!profile)return;
  const label=seasonProfileLabel(profile);if(!confirm(`Permanently delete ${label}? Global macros, play maps, team playbooks, and My Playbook will not be deleted.`))return;
  const wasActive=season.activeProfileId===id;season.profiles=season.profiles.filter(item=>item.id!==id);
  if(wasActive)season.activeProfileId=(season.profiles.find(item=>item.status!=="archived")||season.profiles[0]||{}).id||null;
  season=storeSeasonCommandCenter(season,false);const active=activeSeasonProfile(season);
  applySeasonProfileToWorkingStorage(active||{data:blankSeasonWorkspace("","")});renderAll();
  requestAnimationFrame(()=>el("seasonCommandCenter")?.scrollIntoView({behavior:"smooth",block:"start"}));
}'''
text, count = re.subn(delete_pattern, new_delete, text, count=1, flags=re.S)
if count != 1:
    raise SystemExit(f"Expected one deleteSeasonProfile function, found {count}")

binding_anchor = 'el("jumpSeasonGameplan").onclick=()=>jumpSeasonTo("gameplanPanel");'
binding = binding_anchor + '\nel("deleteActiveSeasonProfile").onclick=()=>{const profile=activeSeasonProfile();if(profile)deleteSeasonProfile(profile.id)};'
if text.count(binding_anchor) != 1:
    raise SystemExit("Season jump binding anchor missing")
text = text.replace(binding_anchor, binding, 1)

# Make the profile-card wording unambiguous.
text = text.replace('seasonActionButton("Delete","remove",()=>deleteSeasonProfile(profile.id))', 'seasonActionButton("Delete Permanently","remove",()=>deleteSeasonProfile(profile.id))', 1)

# Structural and regression validation.
main_pos = text.index('<main class="app">')
handoff_pos = text.index('id="chatGptHandoffPanel"')
season_pos = text.index('id="seasonCommandCenter"')
gameplan_pos = text.index('id="gameplanPanel"')
if not (main_pos < handoff_pos < season_pos < gameplan_pos):
    raise SystemExit("Season Command Center is not positioned between Film Handoff and Weekly Gameplan")

required = [
    'id="deleteActiveSeasonProfile"',
    'Delete Active War Room',
    'Delete Permanently',
    'blankSeasonWorkspace("","")',
    'const teamName=seasonTeamName(opponent)||""',
    'el("deleteActiveSeasonProfile").onclick',
]
for marker in required:
    if text.count(marker) != 1:
        raise SystemExit(f"Expected exactly one marker after patch: {marker}")
if 'const teamName=seasonTeamName(opponent)||"Opponent";' in text:
    raise SystemExit("Generic blank-opponent recreation bug remains")

script = re.search(r'<script>(.*)</script>', text, flags=re.S)
if not script:
    raise SystemExit("Could not extract complete application JavaScript")
Path('/tmp/saturday-war-room-command-center-fix.js').write_text(script.group(1), encoding='utf-8')

path.write_text(text, encoding="utf-8")
print("Command Center placement and permanent-delete fix applied.")
