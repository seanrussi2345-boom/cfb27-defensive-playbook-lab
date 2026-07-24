from html.parser import HTMLParser
from pathlib import Path
import re

INDEX_PATH = Path("index.html")
README_PATH = Path("README.md")
text = INDEX_PATH.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one source block, found {count}")
    text = text.replace(old, new, 1)


navigator_css = r'''
.team-nav-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px}
.team-nav-grid label{margin-top:8px}
.team-nav-actions{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:8px}
.team-nav-actions .favorite-btn{width:100%}
.team-scheme-field[hidden]{display:none}
.team-recent{margin-top:8px;padding:8px;border:1px dashed #35516b;border-radius:9px;background:#0b1723}
.team-recent-title{color:#8fa8bd;font-size:8px;font-weight:850;letter-spacing:.08em;text-transform:uppercase}
.team-recent-list{display:flex;gap:5px;flex-wrap:wrap;margin-top:6px}
.team-recent-chip{padding:5px 7px;border:1px solid #34516b;border-radius:999px;background:#101f2e;color:#dcecff;cursor:pointer;font-size:8px;line-height:1}
.team-recent-chip:hover{border-color:#65d9ef;background:#163249}
.team-result-label{display:flex;align-items:center;justify-content:space-between;gap:8px}
.team-result-label span{color:#7f96ab;font-size:8px;font-weight:700}
@media(max-width:850px){.team-nav-grid,.team-nav-actions{grid-template-columns:1fr}}
'''.strip()
replace_once(
    ".team-playbook-picker[hidden]{display:none}",
    ".team-playbook-picker[hidden]{display:none}\n" + navigator_css,
    "team navigator CSS anchor",
)

old_picker = '''    <div class="team-playbook-picker" id="teamPlaybookPicker" hidden>
      <label>Select Team</label>
      <select id="teamPlaybook">
        <option value="">Select a verified team</option>
      </select>
      <div class="library-count" id="teamPlaybookCount">Select any team to load its CFB 27 defensive playbook.</div>
    </div>'''
new_picker = '''    <div class="team-playbook-picker" id="teamPlaybookPicker" hidden>
      <label>Find Team</label>
      <input id="teamPlaybookSearch" type="search" maxlength="80" placeholder="Search team or defensive scheme…">

      <div class="team-nav-grid">
        <div>
          <label>Browse Teams</label>
          <select id="teamBrowseMode">
            <option value="ALL">All Teams</option>
            <option value="FAVORITES">Favorite Teams</option>
            <option value="RECENT">Recently Viewed</option>
            <option value="SCHEME">By Defensive Scheme</option>
          </select>
        </div>
        <div class="team-scheme-field" id="teamSchemeField" hidden>
          <label>Defensive Scheme</label>
          <select id="teamSchemeFilter"></select>
        </div>
      </div>

      <label class="team-result-label">Team Results <span id="teamNavigatorMatchCount">138 teams</span></label>
      <select id="teamPlaybook" size="5">
        <option value="">Select a verified team</option>
      </select>
      <div class="team-nav-actions">
        <button class="favorite-btn" id="toggleTeamFavorite" type="button">☆ Favorite Team</button>
        <button class="favorite-btn" id="clearTeamNavigator" type="button">Clear Search &amp; Filters</button>
      </div>
      <div class="team-recent" id="teamRecentPanel">
        <div class="team-recent-title">Recently Viewed</div>
        <div class="team-recent-list" id="teamRecentList"></div>
      </div>
      <div class="library-count" id="teamPlaybookCount">Select any team to load its CFB 27 defensive playbook.</div>
    </div>'''
replace_once(old_picker, new_picker, "team playbook picker")

navigator_js = r'''
const TEAM_NAV_STORAGE_KEY="cfb27-playbook-lab-v4-teamnav";
function teamEntriesSorted(){
  return Object.entries(TEAM_PLAYBOOKS).sort(([,a],[,b])=>(a.name||"").localeCompare(b.name||""));
}
function teamSchemeNames(){
  return [...new Set(teamEntriesSorted().map(([,team])=>team.scheme).filter(Boolean))].sort((a,b)=>a.localeCompare(b));
}
function emptyTeamNavigator(){return{favorites:[],recent:[],mode:"ALL",scheme:"",query:""}}
function normalizeTeamNavigator(raw){
  const validIds=new Set(Object.keys(TEAM_PLAYBOOKS)),validModes=new Set(["ALL","FAVORITES","RECENT","SCHEME"]),validSchemes=new Set(teamSchemeNames());
  const uniqueValid=values=>[...new Set(Array.isArray(values)?values:[])].filter(id=>validIds.has(id));
  return {
    favorites:uniqueValid(raw?.favorites),
    recent:uniqueValid(raw?.recent).slice(0,6),
    mode:validModes.has(raw?.mode)?raw.mode:"ALL",
    scheme:validSchemes.has(raw?.scheme)?raw.scheme:"",
    query:typeof raw?.query==="string"?raw.query.slice(0,80):""
  };
}
function getTeamNavigator(){
  try{return normalizeTeamNavigator(JSON.parse(localStorage.getItem(TEAM_NAV_STORAGE_KEY)||"{}"))}
  catch{return emptyTeamNavigator()}
}
function storeTeamNavigator(nav){
  const normalized=normalizeTeamNavigator(nav);localStorage.setItem(TEAM_NAV_STORAGE_KEY,JSON.stringify(normalized));return normalized;
}
function teamNavigatorEntries(nav=getTeamNavigator()){
  const query=nav.query.trim().toUpperCase(),favorites=new Set(nav.favorites),all=teamEntriesSorted();
  let entries=nav.mode==="RECENT"
    ? nav.recent.map(id=>[id,TEAM_PLAYBOOKS[id]]).filter(([,team])=>team)
    : all.filter(([id])=>nav.mode!=="FAVORITES"||favorites.has(id))
         .filter(([,team])=>nav.mode!=="SCHEME"||!nav.scheme||team.scheme===nav.scheme);
  if(query)entries=entries.filter(([,team])=>`${team.name} ${team.scheme}`.toUpperCase().includes(query));
  if(nav.mode==="ALL")entries.sort(([aId,a],[bId,b])=>Number(favorites.has(bId))-Number(favorites.has(aId))||(a.name||"").localeCompare(b.name||""));
  return entries;
}
function populateTeamSchemeFilter(nav=getTeamNavigator()){
  const select=el("teamSchemeFilter"),schemes=teamSchemeNames();select.innerHTML="";
  schemes.forEach(scheme=>{const option=document.createElement("option");option.value=scheme;option.textContent=scheme;select.appendChild(option)});
  const selected=nav.scheme||TEAM_PLAYBOOKS[state.teamPlaybook]?.scheme||schemes[0]||"";
  if(selected&&schemes.includes(selected))select.value=selected;
  return selected;
}
function renderTeamNavigator(){
  const nav=getTeamNavigator(),search=el("teamPlaybookSearch"),mode=el("teamBrowseMode"),schemeField=el("teamSchemeField"),select=el("teamPlaybook");
  if(document.activeElement!==search)search.value=nav.query;
  mode.value=nav.mode;schemeField.hidden=nav.mode!=="SCHEME";
  const selectedScheme=populateTeamSchemeFilter(nav);
  if(nav.mode==="SCHEME"&&!nav.scheme&&selectedScheme){nav.scheme=selectedScheme;storeTeamNavigator(nav)}
  const entries=teamNavigatorEntries(nav),favoriteSet=new Set(nav.favorites);select.innerHTML="";
  if(!entries.length){
    const option=document.createElement("option");option.value="";option.textContent="No teams match the current navigator filters";option.disabled=true;select.appendChild(option);
  }else entries.forEach(([id,team])=>{
    const option=document.createElement("option");option.value=id;option.textContent=`${favoriteSet.has(id)?"★ ":""}${team.name} — ${team.scheme}`;select.appendChild(option);
  });
  if(entries.some(([id])=>id===state.teamPlaybook))select.value=state.teamPlaybook;else select.selectedIndex=-1;
  el("teamNavigatorMatchCount").textContent=`${entries.length} team${entries.length===1?"":"s"}`;
  const favoriteButton=el("toggleTeamFavorite"),isFavorite=!!state.teamPlaybook&&favoriteSet.has(state.teamPlaybook);
  favoriteButton.disabled=!state.teamPlaybook;favoriteButton.classList.toggle("active",isFavorite);favoriteButton.textContent=isFavorite?"★ Favorite Team":"☆ Favorite Team";
  const recentList=el("teamRecentList");recentList.innerHTML="";
  nav.recent.forEach(id=>{
    const team=TEAM_PLAYBOOKS[id];if(!team)return;
    const button=document.createElement("button");button.type="button";button.className="team-recent-chip";button.textContent=team.name;button.title=team.scheme;button.onclick=()=>selectTeamPlaybook(id);recentList.appendChild(button);
  });
  el("teamRecentPanel").hidden=!nav.recent.length;
  const team=activeTeamPlaybook(),totals=teamPlaybookTotals(team);
  el("teamPlaybookCount").textContent=team
    ? `${team.scheme} • ${totals.formations} formations • ${totals.plays} plays • ${entries.length} navigator match${entries.length===1?"":"es"}`
    : `${entries.length} matching team${entries.length===1?"":"s"}`;
}
function selectTeamPlaybook(id){
  if(!TEAM_PLAYBOOKS[id])return;
  state.teamPlaybook=id;
  const nav=getTeamNavigator();nav.recent=[id,...nav.recent.filter(teamId=>teamId!==id)].slice(0,6);storeTeamNavigator(nav);
  ensureVisibleSelection();renderAll();
}
function updateTeamNavigator(patch){
  const nav=getTeamNavigator();Object.assign(nav,patch);storeTeamNavigator(nav);renderTeamNavigator();
}
function toggleCurrentTeamFavorite(){
  if(!state.teamPlaybook)return;
  const nav=getTeamNavigator(),index=nav.favorites.indexOf(state.teamPlaybook);
  if(index>=0)nav.favorites.splice(index,1);else nav.favorites.push(state.teamPlaybook);
  storeTeamNavigator(nav);renderTeamNavigator();
}
function clearTeamNavigator(){
  const nav=getTeamNavigator();nav.mode="ALL";nav.scheme="";nav.query="";storeTeamNavigator(nav);renderTeamNavigator();
}
'''.strip()
replace_once(
    "function availableFamilies(){",
    navigator_js + "\n\nfunction availableFamilies(){",
    "team navigator JavaScript anchor",
)

old_team_render = '''  else if(state.libraryView==="TEAM"){
    const team=activeTeamPlaybook();
    const teamTotals=teamPlaybookTotals(team);
    el("teamPlaybookCount").textContent=team
      ? `${team.scheme} • ${teamTotals.formations} formations • ${teamTotals.plays} plays`
      : "Select a verified team.";
    indicator.innerHTML=`<span>Current view</span><strong>${team?.name||"Team Playbook"}</strong>`;
  }else indicator.innerHTML=`<span>Current view</span><strong>Full Defensive Library</strong>`;'''
new_team_render = '''  else if(state.libraryView==="TEAM"){
    const team=activeTeamPlaybook();renderTeamNavigator();
    indicator.innerHTML=`<span>Current view</span><strong>${team?.name||"Team Playbook"}</strong>`;
  }else indicator.innerHTML=`<span>Current view</span><strong>Full Defensive Library</strong>`;'''
replace_once(old_team_render, new_team_render, "team mode renderer")

old_team_default = '''  if(requested==="TEAM"&&!state.teamPlaybook){
    state.teamPlaybook=Object.entries(TEAM_PLAYBOOKS)
      .sort(([,a],[,b])=>(a.name||"").localeCompare(b.name||""))[0]?.[0]||"";
    el("teamPlaybook").value=state.teamPlaybook;
  }'''
new_team_default = '''  if(requested==="TEAM"&&!state.teamPlaybook){
    const nav=getTeamNavigator();state.teamPlaybook=nav.favorites[0]||nav.recent[0]||teamEntriesSorted()[0]?.[0]||"";
    if(state.teamPlaybook){nav.recent=[state.teamPlaybook,...nav.recent.filter(id=>id!==state.teamPlaybook)].slice(0,6);storeTeamNavigator(nav)}
  }'''
replace_once(old_team_default, new_team_default, "team mode default selection")

old_handler = '''el("teamPlaybook").onchange=e=>{
  state.teamPlaybook=e.target.value;
  ensureVisibleSelection();renderAll();
};'''
new_handler = '''el("teamPlaybook").onchange=e=>selectTeamPlaybook(e.target.value);
el("teamPlaybookSearch").oninput=e=>updateTeamNavigator({query:e.target.value});
el("teamBrowseMode").onchange=e=>updateTeamNavigator({mode:e.target.value});
el("teamSchemeFilter").onchange=e=>updateTeamNavigator({scheme:e.target.value});
el("toggleTeamFavorite").onclick=toggleCurrentTeamFavorite;
el("clearTeamNavigator").onclick=clearTeamNavigator;'''
replace_once(old_handler, new_handler, "team navigator event handlers")

replace_once(
    "    gameplan:getGameplan()\n  };",
    "    gameplan:getGameplan(),\n    teamNavigator:getTeamNavigator()\n  };",
    "backup export payload",
)
replace_once(
    'if(!confirm("Replace the saved macros, play maps, My Playbook list, and weekly gameplan with this backup?"))return;',
    'if(!confirm("Replace the saved macros, play maps, My Playbook list, weekly gameplan, and team navigator with this backup?"))return;',
    "backup import confirmation",
)
replace_once(
    '      storeGameplan(data.gameplan&&typeof data.gameplan==="object"?data.gameplan:emptyGameplan());',
    '      storeGameplan(data.gameplan&&typeof data.gameplan==="object"?data.gameplan:emptyGameplan());\n      storeTeamNavigator(data.teamNavigator&&typeof data.teamNavigator==="object"?data.teamNavigator:emptyTeamNavigator());',
    "backup import storage",
)
replace_once(
    "This deletes every saved macro, play map, My Playbook selection, and weekly gameplan in this browser. Type RESET to continue:",
    "This deletes every saved macro, play map, My Playbook selection, weekly gameplan, and team navigator preference in this browser. Type RESET to continue:",
    "reset confirmation",
)
replace_once(
    '["cfb27-playbook-lab-v4-macros","cfb27-playbook-lab-v4-maps","cfb27-playbook-lab-v4-mybook",GAMEPLAN_STORAGE_KEY]',
    '["cfb27-playbook-lab-v4-macros","cfb27-playbook-lab-v4-maps","cfb27-playbook-lab-v4-mybook",GAMEPLAN_STORAGE_KEY,TEAM_NAV_STORAGE_KEY]',
    "reset storage keys",
)

old_init = '''const sortedTeamEntries=Object.entries(TEAM_PLAYBOOKS).sort(([,a],[,b])=>(a.name||"").localeCompare(b.name||""));
sortedTeamEntries.forEach(([id,book])=>{
  const option=document.createElement("option");option.value=id;option.textContent=book.name||id;el("teamPlaybook").appendChild(option);
});
sortedTeamEntries.forEach(([id,book])=>{
  const option=document.createElement("option");option.value=id;option.textContent=book.name||id;el("gameplanOpponent").appendChild(option);
});'''
new_init = '''const sortedTeamEntries=teamEntriesSorted();
renderTeamNavigator();
sortedTeamEntries.forEach(([id,book])=>{
  const option=document.createElement("option");option.value=id;option.textContent=book.name||id;el("gameplanOpponent").appendChild(option);
});'''
replace_once(old_init, new_init, "team selector initialization")

old_help = '''            <article class="help-card">
              <h3>5. Build a weekly gameplan</h3>
              <p>Select an opponent and situation, then add the current play or a saved macro. Reorder calls, reload them into the field, and print a clean call sheet.</p>
            </article>'''
new_help = '''            <article class="help-card">
              <h3>5. Navigate team playbooks</h3>
              <p>Search all 138 teams, pin favorites, reopen recent teams, or browse every team using the same defensive scheme.</p>
            </article>
            <article class="help-card">
              <h3>6. Build a weekly gameplan</h3>
              <p>Select an opponent and situation, then add the current play or a saved macro. Reorder calls, reload them into the field, and print a clean call sheet.</p>
            </article>'''
replace_once(old_help, new_help, "help navigator card")
replace_once(
    "Use <strong>Import Backup</strong> to transfer macros, play maps, My Playbook, and the weekly gameplan.",
    "Use <strong>Import Backup</strong> to transfer macros, play maps, My Playbook, the weekly gameplan, and team navigator preferences.",
    "help backup description",
)
replace_once(
    '<article class="release-item"><strong>Weekly gameplan builder and printable call sheet</strong>',
    '<article class="release-item"><strong>Searchable team playbook navigator</strong><span>Search all teams, pin favorites, reopen recent playbooks, and browse teams by shared defensive scheme.</span></article>\n            <article class="release-item"><strong>Weekly gameplan builder and printable call sheet</strong>',
    "release note navigator item",
)

INDEX_PATH.write_text(text, encoding="utf-8")

readme = README_PATH.read_text(encoding="utf-8")
readme_marker = "- Team Playbook view for all 138 teams across all 31 defensive books, with exact formation/play membership referencing the existing master play database\n"
readme_feature = "- Searchable Team Playbook Navigator with favorite teams, recently viewed teams, scheme browsing, local persistence, and backup support\n"
if readme_feature not in readme:
    if readme_marker not in readme:
        raise SystemExit("README team-playbook feature marker missing")
    readme = readme.replace(readme_marker, readme_marker + readme_feature, 1)
README_PATH.write_text(readme, encoding="utf-8")


class IdCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []

    def handle_starttag(self, tag, attrs) -> None:
        for key, value in attrs:
            if key == "id" and value:
                self.ids.append(value)


parser = IdCollector()
parser.feed(text)
required_ids = [
    "teamPlaybookSearch",
    "teamBrowseMode",
    "teamSchemeFilter",
    "toggleTeamFavorite",
    "clearTeamNavigator",
    "teamRecentList",
    "teamNavigatorMatchCount",
]
for item in required_ids:
    if parser.ids.count(item) != 1:
        raise SystemExit(f"Expected one #{item}, found {parser.ids.count(item)}")
for item in ["libraryView", "teamPlaybook", "gameplanPanel", "macroList", "field"]:
    if parser.ids.count(item) != 1:
        raise SystemExit(f"Existing control #{item} changed unexpectedly")
required_text = [
    'const TEAM_NAV_STORAGE_KEY="cfb27-playbook-lab-v4-teamnav";',
    "function teamNavigatorEntries",
    "function selectTeamPlaybook",
    "teamNavigator:getTeamNavigator()",
    "storeTeamNavigator(data.teamNavigator",
]
for item in required_text:
    if text.count(item) != 1:
        raise SystemExit(f"Expected one navigator marker: {item}")

script_match = re.search(r"<script>(.*)</script>", text, re.S)
if not script_match:
    raise SystemExit("Could not extract application JavaScript")
Path("/tmp/cfb27-team-navigator.js").write_text(script_match.group(1), encoding="utf-8")
print("Team Playbook Navigator patch and structure validation passed.")
