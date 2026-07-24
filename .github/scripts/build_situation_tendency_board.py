from html.parser import HTMLParser
from pathlib import Path
import re

INDEX = Path("index.html")
README = Path("README.md")
text = INDEX.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one source block, found {count}")
    text = text.replace(old, new, 1)


# ---------- CSS ----------
css = r'''
.tendency-panel{grid-column:1/-1;padding:14px}
.tendency-head{display:flex;align-items:flex-start;justify-content:space-between;gap:14px}
.tendency-head h2{margin-bottom:5px}
.tendency-head .note{margin:0;max-width:590px}
.tendency-layout{display:grid;grid-template-columns:390px minmax(0,1fr);gap:12px;margin-top:12px;align-items:start}
.tendency-builder,.tendency-board{border:1px solid #294159;border-radius:12px;background:#08131f;padding:12px;min-width:0}
.tendency-builder h3,.tendency-board h3{margin:0;color:#eaf7ff;font-size:12px}
.tendency-context{margin-top:7px;padding:8px 9px;border:1px dashed #35516b;border-radius:8px;background:#0b1723;color:#a9c3d8;font-size:9px;line-height:1.45}
.tendency-fields{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.tendency-field.full{grid-column:1/-1}
.tendency-field label{margin-top:9px}
.tendency-field select,.tendency-field textarea{width:100%;padding:9px 10px;color:var(--text);background:#08131f;border:1px solid #304c68;border-radius:9px;outline:none}
.tendency-field textarea{min-height:68px;resize:vertical;font:inherit}
.tendency-field select:focus,.tendency-field textarea:focus{border-color:var(--accent)}
.tendency-actions{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}
.tendency-summary{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin-top:10px}
.tendency-stat{padding:9px;border:1px solid #2e4a63;border-radius:9px;background:#0b1825;min-width:0}
.tendency-stat strong{display:block;color:#eff8ff;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tendency-stat span{display:block;margin-top:3px;color:#8fa8bd;font-size:8px;line-height:1.35}
.tendency-stat.warn{border-color:#7a6334;background:#2b2410}.tendency-stat.good{border-color:#47765a;background:#11261a}
.tendency-filters{display:grid;grid-template-columns:1fr 1fr 1fr;gap:7px;margin-top:10px}
.tendency-filters label{margin-top:0}
.tendency-list{display:grid;gap:8px;margin-top:10px}
.tendency-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:start;padding:10px;border:1px solid #294159;border-radius:10px;background:#0b1825}
.tendency-row.unanswered{border-color:#7a6334;background:#211d11}
.tendency-row-title{display:flex;align-items:center;gap:7px;flex-wrap:wrap}
.tendency-row-title strong{color:#eef7ff;font-size:10px;line-height:1.35}
.frequency-badge{padding:3px 6px;border:1px solid #3b5871;border-radius:999px;background:#102033;color:#cce7f8;font-size:7px;font-weight:900;letter-spacing:.06em;text-transform:uppercase}
.frequency-badge.primary{border-color:#7b434b;background:#29181d;color:#ffc7cd}
.frequency-badge.frequent{border-color:#816a35;background:#2b2410;color:#ffe4a1}
.frequency-badge.occasional{border-color:#47765a;background:#11261a;color:#c9f6d4}
.frequency-badge.alert{border-color:#6b4e86;background:#21172c;color:#e8cfff}
.tendency-row-meta,.tendency-row-note{display:block;margin-top:5px;color:#9fb4c9;font-size:8px;line-height:1.4}
.tendency-row-note{color:#c9d9e7}
.tendency-row-actions{display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end;max-width:250px}
.tendency-row-actions button{padding:5px 7px;border:1px solid #34516b;border-radius:6px;background:#101f2e;color:#dcecff;cursor:pointer;font-size:8px}
.tendency-row-actions button:hover{border-color:#65d9ef}
.tendency-row-actions button:disabled{opacity:.35;cursor:not-allowed}
.tendency-row-actions .remove{border-color:#71424b;background:#29191e;color:#ffc7cd}
.tendency-overuse{margin-top:9px;padding:8px 9px;border:1px solid #7a6334;border-radius:8px;background:#2b2410;color:#ffe4a1;font-size:8px;line-height:1.45}
@media(max-width:1040px){.tendency-layout{grid-template-columns:1fr}.tendency-summary{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media(max-width:700px){.tendency-head{display:block}.tendency-head .note{margin-top:8px}.tendency-fields,.tendency-filters,.tendency-summary{grid-template-columns:1fr}.tendency-row{grid-template-columns:1fr}.tendency-row-actions{justify-content:flex-start;max-width:none}}
'''.strip()
replace_once(
    ".gameplan-panel{grid-column:1/-1;padding:14px}",
    css + "\n\n.gameplan-panel{grid-column:1/-1;padding:14px}",
    "tendency board CSS",
)
replace_once(
    "header,.left,.center,.right,.macro-panel,.scout-panel,.gameplan-builder,.gameplan-actions,.entry-actions,.gameplan-help,.modal-backdrop,footer{display:none!important}",
    "header,.left,.center,.right,.macro-panel,.scout-panel,.tendency-panel,.gameplan-builder,.gameplan-actions,.entry-actions,.gameplan-help,.modal-backdrop,footer{display:none!important}",
    "print visibility",
)

# ---------- HTML ----------
panel = r'''
  <section class="panel tendency-panel" id="tendencyBoardPanel">
    <div class="tendency-head">
      <div>
        <h2>Situation-Based Opponent Tendency Board</h2>
        <div class="helptext">Organize the opponent by situation, personnel, set, and base concept, then attach a primary macro and an optional changeup answer.</div>
      </div>
      <div class="note">This is one active opponent board. It references saved macro slots without changing the original macro builder or Scout Lab selections.</div>
    </div>

    <div class="tendency-layout">
      <div class="tendency-builder">
        <h3 id="tendencyBuilderTitle">Add Opponent Tendency</h3>
        <div class="tendency-context" id="tendencyBoardContext">Generic opponent board</div>
        <div class="tendency-fields">
          <div class="tendency-field">
            <label>Situation</label>
            <select id="tendencySituation">
              <option>Base Defense</option><option>1st &amp; 10</option><option>2nd &amp; Short</option><option>2nd &amp; Medium</option><option>2nd &amp; Long</option><option>3rd &amp; Short</option><option>3rd &amp; Medium</option><option>3rd &amp; Long</option><option>Red Zone</option><option>Goal Line</option><option>Two-Minute</option><option>Backed Up</option><option>RPO</option><option>Empty</option><option>Bunch / Trips</option><option>Run Heavy</option><option>Custom</option>
            </select>
          </div>
          <div class="tendency-field">
            <label>Frequency</label>
            <select id="tendencyFrequency"><option>Primary</option><option selected>Frequent</option><option>Occasional</option><option>Alert</option></select>
          </div>
          <div class="tendency-field">
            <label>Personnel</label>
            <select id="tendencyPersonnel"><option>10</option><option selected>11</option><option>12</option><option>13</option><option>20</option><option>21</option><option>22</option><option>Other</option></select>
          </div>
          <div class="tendency-field">
            <label>Passing Strength</label>
            <select id="tendencyStrength"><option value="left">Left</option><option value="right" selected>Right</option></select>
          </div>
          <div class="tendency-field">
            <label>Offensive Set</label>
            <select id="tendencySet"></select>
          </div>
          <div class="tendency-field">
            <label>Base Concept</label>
            <select id="tendencyConcept"></select>
          </div>
          <div class="tendency-field">
            <label>Primary Defensive Macro</label>
            <select id="tendencyPrimaryMacro"></select>
          </div>
          <div class="tendency-field">
            <label>Changeup Macro</label>
            <select id="tendencyChangeupMacro"></select>
          </div>
          <div class="tendency-field full">
            <label>Danger Player / Motion / Formation Alert</label>
            <textarea id="tendencyAlert" maxlength="180" placeholder="Slot motion, RB wheel, best player at X, fast tempo after explosives…"></textarea>
          </div>
          <div class="tendency-field full">
            <label>Defensive Coaching Note</label>
            <textarea id="tendencyNote" maxlength="260" placeholder="User defender, leverage rule, pressure check, force player, coverage adjustment…"></textarea>
          </div>
        </div>
        <div class="tendency-actions">
          <button class="scout-btn" id="seedTendencyFromScout" type="button">Use Current Scout Selection</button>
          <button class="scout-btn primary" id="saveTendency" type="button">Add Tendency</button>
          <button class="scout-btn" id="cancelTendencyEdit" type="button" hidden>Cancel Edit</button>
          <button class="scout-btn warn" id="newTendencyBoard" type="button">New Blank Board</button>
        </div>
      </div>

      <div class="tendency-board">
        <div class="scout-saved-head"><strong>Opponent Situation Board</strong><span class="call-sheet-count" id="tendencyCount">0 tendencies</span></div>
        <div class="tendency-summary" id="tendencySummary"></div>
        <div class="tendency-overuse" id="tendencyOveruse" hidden></div>
        <div class="tendency-filters">
          <div class="tendency-field"><label>Situation Filter</label><select id="tendencyFilterSituation"><option value="ALL">All Situations</option></select></div>
          <div class="tendency-field"><label>Frequency Filter</label><select id="tendencyFilterFrequency"><option value="ALL">All Frequencies</option><option>Primary</option><option>Frequent</option><option>Occasional</option><option>Alert</option></select></div>
          <div class="tendency-field"><label>Answer Filter</label><select id="tendencyFilterAnswer"><option value="ALL">All Answers</option><option value="ANSWERED">Primary Assigned</option><option value="UNANSWERED">Needs Primary Answer</option></select></div>
        </div>
        <div class="tendency-list" id="tendencyList"></div>
      </div>
    </div>
  </section>
'''.strip()
replace_once(
    '  <section class="panel gameplan-panel" id="gameplanPanel">',
    panel + '\n\n  <section class="panel gameplan-panel" id="gameplanPanel">',
    "tendency board panel",
)

# ---------- JavaScript ----------
js = r'''
const TENDENCY_STORAGE_KEY="cfb27-playbook-lab-v4-tendency-board";
const TENDENCY_SITUATIONS=["Base Defense","1st & 10","2nd & Short","2nd & Medium","2nd & Long","3rd & Short","3rd & Medium","3rd & Long","Red Zone","Goal Line","Two-Minute","Backed Up","RPO","Empty","Bunch / Trips","Run Heavy","Custom"];
const TENDENCY_FREQUENCIES=["Primary","Frequent","Occasional","Alert"];
const TENDENCY_PERSONNEL=["10","11","12","13","20","21","22","Other"];
const TENDENCY_WEIGHTS={Primary:4,Frequent:3,Occasional:2,Alert:1};
let tendencyEditingId=null;

function emptyTendencyBoard(){const scout=getScoutReport();return{opponent:scout.opponent||"",week:scout.week||"",entries:[],filters:{situation:"ALL",frequency:"ALL",answer:"ALL"},updatedAt:null}}
function normalizeTendencyBoard(raw){
  const base=emptyTendencyBoard(),validSets=new Set(Object.keys(OFFENSIVE_SCOUT_SETS)),validConcepts=new Set(Object.keys(OFFENSIVE_SCOUT_CONCEPTS)),validSituations=new Set(TENDENCY_SITUATIONS),validFrequencies=new Set(TENDENCY_FREQUENCIES),validPersonnel=new Set(TENDENCY_PERSONNEL);
  const entries=(Array.isArray(raw?.entries)?raw.entries:[]).filter(item=>item&&validSets.has(item.set)&&validConcepts.has(item.concept)).slice(-80).map((item,index)=>({
    id:String(item.id||`tendency-${index}-${Date.now()}`),
    situation:validSituations.has(item.situation)?item.situation:"Base Defense",
    frequency:validFrequencies.has(item.frequency)?item.frequency:"Frequent",
    personnel:validPersonnel.has(String(item.personnel))?String(item.personnel):OFFENSIVE_SCOUT_SETS[item.set]?.personnel||"11",
    set:item.set,concept:item.concept,strength:item.strength==="left"?"left":"right",
    primaryMacroSlot:Number.isInteger(item.primaryMacroSlot)&&item.primaryMacroSlot>=0&&item.primaryMacroSlot<10?item.primaryMacroSlot:null,
    changeupMacroSlot:Number.isInteger(item.changeupMacroSlot)&&item.changeupMacroSlot>=0&&item.changeupMacroSlot<10?item.changeupMacroSlot:null,
    alert:typeof item.alert==="string"?item.alert.slice(0,180):"",
    note:typeof item.note==="string"?item.note.slice(0,260):"",
    gameplanRoles:Array.isArray(item.gameplanRoles)?item.gameplanRoles.filter(role=>role==="Primary"||role==="Changeup"):[],
    createdAt:item.createdAt||new Date().toISOString()
  }));
  const filters=raw?.filters&&typeof raw.filters==="object"?raw.filters:{};
  return{...base,...raw,opponent:TEAM_PLAYBOOKS[raw?.opponent]?raw.opponent:"",week:typeof raw?.week==="string"?raw.week.slice(0,80):"",entries,filters:{situation:filters.situation==="ALL"||validSituations.has(filters.situation)?filters.situation:"ALL",frequency:filters.frequency==="ALL"||validFrequencies.has(filters.frequency)?filters.frequency:"ALL",answer:["ALL","ANSWERED","UNANSWERED"].includes(filters.answer)?filters.answer:"ALL"}};
}
function getTendencyBoard(){try{return normalizeTendencyBoard(JSON.parse(localStorage.getItem(TENDENCY_STORAGE_KEY)||"{}"))}catch{return emptyTendencyBoard()}}
function storeTendencyBoard(board){const normalized=normalizeTendencyBoard(board);normalized.updatedAt=new Date().toISOString();localStorage.setItem(TENDENCY_STORAGE_KEY,JSON.stringify(normalized));return normalized}
function tendencyMacro(slot){return Number.isInteger(slot)?getMacros()[slot]||null:null}
function tendencyMacroLabel(slot){const macro=tendencyMacro(slot);return macro?`${String(slot+1).padStart(2,"0")} — ${macro.name}`:"Unassigned"}
function tendencyAnswered(entry){return!!tendencyMacro(entry.primaryMacroSlot)}

function fillTendencySetOptions(){
  const select=el("tendencySet"),current=select.value;select.innerHTML="";
  Object.entries(OFFENSIVE_SCOUT_SETS).forEach(([id,set])=>{const option=document.createElement("option");option.value=id;option.textContent=`${set.name} — ${set.personnel} personnel`;select.appendChild(option)});
  select.value=OFFENSIVE_SCOUT_SETS[current]?current:getScoutReport().set||"gun2x2";
}
function fillTendencyConceptOptions(){
  const select=el("tendencyConcept"),current=select.value;select.innerHTML="";
  OFFENSIVE_CONCEPT_CATEGORIES.forEach(category=>{const group=document.createElement("optgroup");group.label=category;Object.entries(OFFENSIVE_SCOUT_CONCEPTS).filter(([,concept])=>concept.category===category).forEach(([id,concept])=>{const option=document.createElement("option");option.value=id;option.textContent=concept.name;group.appendChild(option)});select.appendChild(group)});
  select.value=OFFENSIVE_SCOUT_CONCEPTS[current]?current:getScoutReport().concept||"fourVerticals";
}
function fillTendencyMacroSelect(id){
  const select=el(id),current=select.value;select.innerHTML="";const blank=document.createElement("option");blank.value="";blank.textContent="Unassigned";select.appendChild(blank);
  getMacros().forEach((macro,index)=>{if(!macro)return;const option=document.createElement("option");option.value=String(index);option.textContent=`${String(index+1).padStart(2,"0")} — ${macro.name} | ${macro.formation} — ${macro.play}`;select.appendChild(option)});
  if([...select.options].some(option=>option.value===current))select.value=current;else select.value="";
}
function populateTendencyFilters(board=getTendencyBoard()){
  const situation=el("tendencyFilterSituation"),current=board.filters.situation;situation.innerHTML='<option value="ALL">All Situations</option>';TENDENCY_SITUATIONS.forEach(value=>{const option=document.createElement("option");option.value=value;option.textContent=value;situation.appendChild(option)});situation.value=current;
  el("tendencyFilterFrequency").value=board.filters.frequency;el("tendencyFilterAnswer").value=board.filters.answer;
}
function seedTendencyFormFromScout(){
  const report=getScoutReport(),set=OFFENSIVE_SCOUT_SETS[report.set];fillTendencySetOptions();fillTendencyConceptOptions();fillTendencyMacroSelect("tendencyPrimaryMacro");fillTendencyMacroSelect("tendencyChangeupMacro");
  el("tendencySituation").value=TENDENCY_SITUATIONS.includes(report.situation)?report.situation:"Base Defense";el("tendencyPersonnel").value=TENDENCY_PERSONNEL.includes(set?.personnel)?set.personnel:"11";el("tendencySet").value=report.set;el("tendencyConcept").value=report.concept;el("tendencyStrength").value=report.strength;el("tendencyPrimaryMacro").value=Number.isInteger(report.macroSlot)&&tendencyMacro(report.macroSlot)?String(report.macroSlot):"";
}
function resetTendencyForm(useScout=true){
  tendencyEditingId=null;el("tendencyBuilderTitle").textContent="Add Opponent Tendency";el("saveTendency").textContent="Add Tendency";el("cancelTendencyEdit").hidden=true;el("tendencyFrequency").value="Frequent";el("tendencyChangeupMacro").value="";el("tendencyAlert").value="";el("tendencyNote").value="";if(useScout)seedTendencyFormFromScout();else{el("tendencySituation").value="Base Defense";el("tendencyPersonnel").value="11";el("tendencyStrength").value="right";el("tendencyPrimaryMacro").value=""}
}
function tendencyFormEntry(existing=null){
  return{id:existing?.id||`tendency-${Date.now()}-${Math.random().toString(36).slice(2,8)}`,situation:el("tendencySituation").value,frequency:el("tendencyFrequency").value,personnel:el("tendencyPersonnel").value,set:el("tendencySet").value,concept:el("tendencyConcept").value,strength:el("tendencyStrength").value,primaryMacroSlot:el("tendencyPrimaryMacro").value===""?null:Number(el("tendencyPrimaryMacro").value),changeupMacroSlot:el("tendencyChangeupMacro").value===""?null:Number(el("tendencyChangeupMacro").value),alert:el("tendencyAlert").value.trim(),note:el("tendencyNote").value.trim(),gameplanRoles:existing?.gameplanRoles||[],createdAt:existing?.createdAt||new Date().toISOString()};
}
function saveTendencyFromForm(){
  const board=getTendencyBoard(),existing=tendencyEditingId?board.entries.find(entry=>entry.id===tendencyEditingId):null,entry=tendencyFormEntry(existing);if(!OFFENSIVE_SCOUT_SETS[entry.set]||!OFFENSIVE_SCOUT_CONCEPTS[entry.concept]){alert("Select a valid offensive set and concept.");return}
  if(!board.entries.length){const report=getScoutReport();board.opponent=report.opponent;board.week=report.week}
  if(existing)board.entries=board.entries.map(item=>item.id===existing.id?entry:item);else board.entries.push(entry);storeTendencyBoard(board);resetTendencyForm();renderTendencyBoard();
}
function editTendency(id){
  const entry=getTendencyBoard().entries.find(item=>item.id===id);if(!entry)return;tendencyEditingId=id;fillTendencySetOptions();fillTendencyConceptOptions();fillTendencyMacroSelect("tendencyPrimaryMacro");fillTendencyMacroSelect("tendencyChangeupMacro");el("tendencyBuilderTitle").textContent="Edit Opponent Tendency";el("saveTendency").textContent="Update Tendency";el("cancelTendencyEdit").hidden=false;el("tendencySituation").value=entry.situation;el("tendencyFrequency").value=entry.frequency;el("tendencyPersonnel").value=entry.personnel;el("tendencySet").value=entry.set;el("tendencyConcept").value=entry.concept;el("tendencyStrength").value=entry.strength;el("tendencyPrimaryMacro").value=Number.isInteger(entry.primaryMacroSlot)?String(entry.primaryMacroSlot):"";el("tendencyChangeupMacro").value=Number.isInteger(entry.changeupMacroSlot)?String(entry.changeupMacroSlot):"";el("tendencyAlert").value=entry.alert;el("tendencyNote").value=entry.note;el("tendencyBuilderTitle").scrollIntoView({behavior:"smooth",block:"center"});
}
function removeTendency(id){const board=getTendencyBoard();board.entries=board.entries.filter(entry=>entry.id!==id);storeTendencyBoard(board);if(tendencyEditingId===id)resetTendencyForm();renderTendencyBoard()}
function newBlankTendencyBoard(){const board=getTendencyBoard();if(board.entries.length&&!confirm("Start a new blank opponent tendency board and remove the current tendencies?"))return;storeTendencyBoard(emptyTendencyBoard());resetTendencyForm();renderTendencyBoard()}
function loadTendencyIntoScout(id,role="Primary"){
  const entry=getTendencyBoard().entries.find(item=>item.id===id);if(!entry)return;const slot=role==="Changeup"?entry.changeupMacroSlot:entry.primaryMacroSlot,report=getScoutReport();report.set=entry.set;report.concept=entry.concept;report.strength=entry.strength;report.situation=entry.situation;report.macroSlot=tendencyMacro(slot)?slot:null;scoutPreviewPackage=null;storeScoutReport(report);renderScoutReport();el("scoutLabPanel")?.scrollIntoView({behavior:"smooth",block:"start"});
}
function addTendencyToGameplan(id,role="Primary"){
  const board=getTendencyBoard(),entry=board.entries.find(item=>item.id===id);if(!entry)return;const slot=role==="Changeup"?entry.changeupMacroSlot:entry.primaryMacroSlot,macro=tendencyMacro(slot);if(!macro){alert(`Assign an available ${role.toLowerCase()} macro before adding this tendency to the gameplan.`);return}
  const set=OFFENSIVE_SCOUT_SETS[entry.set],concept=OFFENSIVE_SCOUT_CONCEPTS[entry.concept],plan=getGameplan();if(board.opponent)plan.opponent=board.opponent;if(board.week)plan.week=board.week;plan.entries.push({id:`call-${Date.now()}-${Math.random().toString(36).slice(2,8)}`,situation:entry.situation,note:[`vs ${set.name} • ${concept.name} • ${entry.personnel} personnel • ${entry.frequency}`,entry.alert,entry.note].filter(Boolean).join(" • ").slice(0,220),source:`Tendency Board ${role}: Macro ${String(slot+1).padStart(2,"0")} — ${macro.name}`,macroSlot:slot,package:clonePackage(macro)});storeGameplan(plan);entry.gameplanRoles=[...new Set([...(entry.gameplanRoles||[]),role])];storeTendencyBoard(board);renderGameplan();renderTendencyBoard();
}
function updateTendencyFilter(key,value){const board=getTendencyBoard();board.filters[key]=value;storeTendencyBoard(board);renderTendencyBoard()}
function weightedTop(entries,key,labeler=value=>value){
  const scores=new Map();entries.forEach(entry=>{const value=entry[key],weight=TENDENCY_WEIGHTS[entry.frequency]||1;scores.set(value,(scores.get(value)||0)+weight)});const top=[...scores.entries()].sort((a,b)=>b[1]-a[1])[0];return top?labeler(top[0]):"—";
}
function renderTendencySummary(board){
  const summary=el("tendencySummary");summary.innerHTML="";const answered=board.entries.filter(tendencyAnswered).length,gameplanned=board.entries.filter(entry=>(entry.gameplanRoles||[]).length).length,topPersonnel=weightedTop(board.entries,"personnel"),topSet=weightedTop(board.entries,"set",id=>OFFENSIVE_SCOUT_SETS[id]?.name||id),topConcept=weightedTop(board.entries,"concept",id=>OFFENSIVE_SCOUT_CONCEPTS[id]?.name||id),stats=[[String(board.entries.length),"Total tendencies",""],[`${answered}/${board.entries.length}`,"Primary answers",answered===board.entries.length&&board.entries.length?"good":board.entries.length?"warn":""],[String(gameplanned),"Added to gameplan",""],[topPersonnel,"Top personnel",""],[topSet,"Top set",""],[topConcept,"Top concept",""]];stats.forEach(([value,label,className])=>{const card=document.createElement("div");card.className=`tendency-stat ${className}`.trim();const strong=document.createElement("strong"),span=document.createElement("span");strong.textContent=value;span.textContent=label;card.append(strong,span);summary.appendChild(card)});
  const usage=new Map();board.entries.forEach(entry=>{if(tendencyMacro(entry.primaryMacroSlot))usage.set(entry.primaryMacroSlot,(usage.get(entry.primaryMacroSlot)||0)+1)});const top=[...usage.entries()].sort((a,b)=>b[1]-a[1])[0],overuse=el("tendencyOveruse");if(top&&board.entries.length>=4&&top[1]>=Math.max(3,Math.ceil(board.entries.length*.5))){overuse.hidden=false;overuse.textContent=`Macro ${String(top[0]+1).padStart(2,"0")} is the primary answer for ${top[1]} of ${board.entries.length} tendencies. Consider a changeup to avoid overusing one call.`}else{overuse.hidden=true;overuse.textContent=""}
}
function renderTendencyBoard(){
  const board=getTendencyBoard(),report=getScoutReport();fillTendencySetOptions();fillTendencyConceptOptions();fillTendencyMacroSelect("tendencyPrimaryMacro");fillTendencyMacroSelect("tendencyChangeupMacro");populateTendencyFilters(board);const opponent=TEAM_PLAYBOOKS[board.opponent]?.name||"Generic opponent",context=[opponent,board.week].filter(Boolean).join(" • ");el("tendencyBoardContext").textContent=`Board: ${context}${board.entries.length?"":" • Current Scout Lab selections will seed new tendencies."}`;el("tendencyCount").textContent=`${board.entries.length} tendenc${board.entries.length===1?"y":"ies"}`;renderTendencySummary(board);
  const filtered=board.entries.filter(entry=>board.filters.situation==="ALL"||entry.situation===board.filters.situation).filter(entry=>board.filters.frequency==="ALL"||entry.frequency===board.filters.frequency).filter(entry=>board.filters.answer==="ALL"||(board.filters.answer==="ANSWERED"&&tendencyAnswered(entry))||(board.filters.answer==="UNANSWERED"&&!tendencyAnswered(entry))).sort((a,b)=>TENDENCY_SITUATIONS.indexOf(a.situation)-TENDENCY_SITUATIONS.indexOf(b.situation)||(TENDENCY_WEIGHTS[b.frequency]||0)-(TENDENCY_WEIGHTS[a.frequency]||0));
  const list=el("tendencyList");list.innerHTML="";if(!filtered.length){const empty=document.createElement("div");empty.className="empty-state";empty.textContent=board.entries.length?"No tendencies match the current filters.":"No opponent tendencies saved yet. Use the current Scout Lab selection or build one here.";list.appendChild(empty);return}
  filtered.forEach(entry=>{const set=OFFENSIVE_SCOUT_SETS[entry.set],concept=OFFENSIVE_SCOUT_CONCEPTS[entry.concept],row=document.createElement("article");row.className=`tendency-row${tendencyAnswered(entry)?"":" unanswered"}`;const main=document.createElement("div"),title=document.createElement("div");title.className="tendency-row-title";const badge=document.createElement("span");badge.className=`frequency-badge ${entry.frequency.toLowerCase()}`;badge.textContent=entry.frequency;const strong=document.createElement("strong");strong.textContent=`${entry.situation} — ${set.name} — ${concept.name}`;title.append(badge,strong);const meta=document.createElement("span");meta.className="tendency-row-meta";meta.textContent=`Personnel ${entry.personnel} • Strength ${entry.strength.toUpperCase()} • Primary: ${tendencyMacroLabel(entry.primaryMacroSlot)} • Changeup: ${tendencyMacroLabel(entry.changeupMacroSlot)}`;main.append(title,meta);if(entry.alert||entry.note){const note=document.createElement("span");note.className="tendency-row-note";note.textContent=[entry.alert&&`Alert: ${entry.alert}`,entry.note].filter(Boolean).join(" • ");main.appendChild(note)}const actions=document.createElement("div");actions.className="tendency-row-actions";const make=(label,handler,disabled=false,className="")=>{const button=document.createElement("button");button.type="button";button.textContent=label;button.disabled=disabled;button.className=className;button.onclick=handler;return button};actions.append(make("Edit",()=>editTendency(entry.id)),make("Primary Lab",()=>loadTendencyIntoScout(entry.id,"Primary"),!tendencyMacro(entry.primaryMacroSlot)),make("Changeup Lab",()=>loadTendencyIntoScout(entry.id,"Changeup"),!tendencyMacro(entry.changeupMacroSlot)),make((entry.gameplanRoles||[]).includes("Primary")?"Primary Added":"Add Primary",()=>addTendencyToGameplan(entry.id,"Primary"),!tendencyMacro(entry.primaryMacroSlot)||(entry.gameplanRoles||[]).includes("Primary")),make((entry.gameplanRoles||[]).includes("Changeup")?"Changeup Added":"Add Changeup",()=>addTendencyToGameplan(entry.id,"Changeup"),!tendencyMacro(entry.changeupMacroSlot)||(entry.gameplanRoles||[]).includes("Changeup")),make("Remove",()=>removeTendency(entry.id),false,"remove"));row.append(main,actions);list.appendChild(row)});
}
'''.strip()
replace_once(
    "function clearScoutReport(){const report=getScoutReport();if((report.notes||report.concepts||report.matchups.length)&&!confirm(\"Start a new blank opponent scout report?\"))return;scoutPreviewPackage=null;storeScoutReport(emptyScoutReport());renderScoutReport()}\n\nfunction getMacros(){",
    "function clearScoutReport(){const report=getScoutReport();if((report.notes||report.concepts||report.matchups.length)&&!confirm(\"Start a new blank opponent scout report?\"))return;scoutPreviewPackage=null;storeScoutReport(emptyScoutReport());renderScoutReport()}\n\n" + js + "\n\nfunction getMacros(){",
    "tendency board JavaScript",
)
replace_once(
    "function renderAll(){\n  updateTypeBadge();renderField();renderPlayerGrid();renderAssignmentGroups();renderSummary();renderMapping();renderMacros();renderFavoriteControls();renderUndo();renderGameplan();renderScoutReport();\n}",
    "function renderAll(){\n  updateTypeBadge();renderField();renderPlayerGrid();renderAssignmentGroups();renderSummary();renderMapping();renderMacros();renderFavoriteControls();renderUndo();renderGameplan();renderScoutReport();renderTendencyBoard();\n}",
    "render tendency board",
)
replace_once(
    "data[idx]=snapshot(name);storeMacros(data);state.selectedSlot=idx;renderMacros();",
    "data[idx]=snapshot(name);storeMacros(data);state.selectedSlot=idx;renderMacros();renderScoutReport();renderTendencyBoard();",
    "refresh tendency after macro save",
)
replace_once(
    "data[state.selectedSlot]=snapshot(name);storeMacros(data);renderMacros();",
    "data[state.selectedSlot]=snapshot(name);storeMacros(data);renderMacros();renderScoutReport();renderTendencyBoard();",
    "refresh tendency after macro overwrite",
)

bindings = r'''
el("seedTendencyFromScout").onclick=()=>{tendencyEditingId=null;resetTendencyForm();};
el("saveTendency").onclick=saveTendencyFromForm;
el("cancelTendencyEdit").onclick=()=>{resetTendencyForm();renderTendencyBoard()};
el("newTendencyBoard").onclick=newBlankTendencyBoard;
el("tendencySet").onchange=()=>{const set=OFFENSIVE_SCOUT_SETS[el("tendencySet").value];if(set&&TENDENCY_PERSONNEL.includes(set.personnel))el("tendencyPersonnel").value=set.personnel};
el("tendencyFilterSituation").onchange=e=>updateTendencyFilter("situation",e.target.value);
el("tendencyFilterFrequency").onchange=e=>updateTendencyFilter("frequency",e.target.value);
el("tendencyFilterAnswer").onchange=e=>updateTendencyFilter("answer",e.target.value);
'''.strip()
replace_once(
    'el("clearScoutReport").onclick=clearScoutReport;\n\nfunction exportBackup(){',
    'el("clearScoutReport").onclick=clearScoutReport;\n\n' + bindings + '\n\nfunction exportBackup(){',
    "tendency board event bindings",
)

# ---------- Backup, reset, help, release notes ----------
replace_once(
    "    scoutReport:getScoutReport()\n  };",
    "    scoutReport:getScoutReport(),\n    tendencyBoard:getTendencyBoard()\n  };",
    "backup export",
)
replace_once(
    'if(!confirm("Replace the saved macros, play maps, My Playbook list, weekly gameplan, team navigator, and opponent scout report with this backup?"))return;',
    'if(!confirm("Replace the saved macros, play maps, My Playbook list, weekly gameplan, team navigator, opponent scout report, and tendency board with this backup?"))return;',
    "backup import confirmation",
)
replace_once(
    "      storeScoutReport(data.scoutReport&&typeof data.scoutReport===\"object\"?data.scoutReport:emptyScoutReport());",
    "      storeScoutReport(data.scoutReport&&typeof data.scoutReport===\"object\"?data.scoutReport:emptyScoutReport());\n      storeTendencyBoard(data.tendencyBoard&&typeof data.tendencyBoard===\"object\"?data.tendencyBoard:emptyTendencyBoard());",
    "backup import storage",
)
replace_once(
    'const confirmation=prompt("This deletes every saved macro, play map, My Playbook selection, weekly gameplan, team navigator preference, and opponent scout report in this browser. Type RESET to continue:");',
    'const confirmation=prompt("This deletes every saved macro, play map, My Playbook selection, weekly gameplan, team navigator preference, opponent scout report, and tendency board in this browser. Type RESET to continue:");',
    "reset confirmation",
)
replace_once(
    '["cfb27-playbook-lab-v4-macros","cfb27-playbook-lab-v4-maps","cfb27-playbook-lab-v4-mybook",GAMEPLAN_STORAGE_KEY,TEAM_NAV_STORAGE_KEY,SCOUT_STORAGE_KEY].forEach(key=>localStorage.removeItem(key));',
    '["cfb27-playbook-lab-v4-macros","cfb27-playbook-lab-v4-maps","cfb27-playbook-lab-v4-mybook",GAMEPLAN_STORAGE_KEY,TEAM_NAV_STORAGE_KEY,SCOUT_STORAGE_KEY,TENDENCY_STORAGE_KEY].forEach(key=>localStorage.removeItem(key));',
    "reset tendency storage",
)
replace_once(
    '<article class="help-card">\n              <h3>7. Build a weekly gameplan</h3>\n              <p>Select an opponent and situation, then add the current play, a saved macro, or a tested scout-lab matchup. Reorder calls, reload them into the field, and print a clean call sheet.</p>\n            </article>',
    '<article class="help-card">\n              <h3>7. Build the tendency board</h3>\n              <p>Save situation, personnel, offensive set, and concept tendencies, then attach a primary macro and optional changeup before sending either answer to the Weekly Gameplan.</p>\n            </article>\n            <article class="help-card">\n              <h3>8. Build a weekly gameplan</h3>\n              <p>Select an opponent and situation, then add the current play, a saved macro, a tested scout-lab matchup, or a tendency-board answer. Reorder calls, reload them into the field, and print a clean call sheet.</p>\n            </article>',
    "help tendency board",
)
replace_once(
    'Use <strong>Import Backup</strong> to transfer macros, play maps, My Playbook, the weekly gameplan, team navigator preferences, and the opponent scout report.',
    'Use <strong>Import Backup</strong> to transfer macros, play maps, My Playbook, the weekly gameplan, team navigator preferences, the opponent scout report, and the tendency board.',
    "help backup wording",
)
replace_once(
    '<div class="release-list">',
    '<div class="release-list">\n            <article class="release-item"><strong>Situation-based opponent tendency board</strong><span>Organize tendencies by situation, frequency, personnel, set, and base concept; attach primary and changeup macros; identify unanswered calls and macro overuse; preview answers in the Scout Lab; and send them to the Weekly Gameplan.</span></article>',
    "release note",
)

INDEX.write_text(text, encoding="utf-8")
readme = README.read_text(encoding="utf-8")
marker = "- Base Offensive Concept layer with grouped pass, run, option, screen, and RPO selections; route/run visualization; concept-specific defensive stress alerts; and concept metadata preserved in saved scout matchups and Weekly Gameplan calls\n"
feature = "- Situation-Based Opponent Tendency Board with situation/frequency/personnel organization, primary and changeup macro answers, unanswered-call and macro-overuse summaries, Scout Lab preview, Weekly Gameplan integration, local persistence, and backup support\n"
if feature not in readme:
    if marker not in readme:
        raise SystemExit("README offensive concept marker missing")
    readme = readme.replace(marker, marker + feature, 1)
README.write_text(readme, encoding="utf-8")

# ---------- Validation ----------
class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key=="id" and value:self.ids.append(value)

parser=IdCollector();parser.feed(text)
new_ids=["tendencyBoardPanel","tendencyBoardContext","tendencySituation","tendencyFrequency","tendencyPersonnel","tendencyStrength","tendencySet","tendencyConcept","tendencyPrimaryMacro","tendencyChangeupMacro","tendencyAlert","tendencyNote","seedTendencyFromScout","saveTendency","cancelTendencyEdit","newTendencyBoard","tendencyCount","tendencySummary","tendencyOveruse","tendencyFilterSituation","tendencyFilterFrequency","tendencyFilterAnswer","tendencyList"]
for item in new_ids:
    if parser.ids.count(item)!=1:raise SystemExit(f"Expected exactly one #{item}, found {parser.ids.count(item)}")
preserved=["libraryView","family","formation","play","field","playerGrid","assignmentGroups","macroList","saveMacro","overwriteMacro","clearMacros","scoutLabPanel","scoutOffensiveSet","scoutConcept","scoutMacro","scoutField","gameplanPanel","gameplanCallSheet"]
for item in preserved:
    if parser.ids.count(item)!=1:raise SystemExit(f"Fundamental existing control #{item} changed unexpectedly")
required=["const TENDENCY_STORAGE_KEY=","function renderTendencyBoard()","function addTendencyToGameplan","function loadTendencyIntoScout","tendencyBoard:getTendencyBoard()","renderTendencyBoard();"]
for item in required:
    if text.count(item)<1:raise SystemExit(f"Missing tendency-board integration marker: {item}")
script=re.search(r"<script>(.*)</script>",text,re.S)
if not script:raise SystemExit("Could not extract application JavaScript")
Path("/tmp/cfb27-tendency-board.js").write_text(script.group(1),encoding="utf-8")
print("Situation-based opponent tendency board patch validation passed.")
