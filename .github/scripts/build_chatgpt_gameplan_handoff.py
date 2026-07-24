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
.handoff-panel{grid-column:1/-1;padding:14px}
.handoff-head{display:flex;align-items:flex-start;justify-content:space-between;gap:14px}
.handoff-head h2{margin-bottom:5px}
.handoff-head .note{margin:0;max-width:600px}
.handoff-layout{display:grid;grid-template-columns:430px minmax(0,1fr);gap:12px;margin-top:12px;align-items:start}
.handoff-input,.handoff-output{border:1px solid #294159;border-radius:12px;background:#08131f;padding:12px;min-width:0}
.handoff-input h3,.handoff-output h3{margin:0;color:#eaf7ff;font-size:12px}
.handoff-fields{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.handoff-field.full{grid-column:1/-1}
.handoff-field label{margin-top:9px}
.handoff-field input[type="text"],.handoff-field input[type="url"],.handoff-field textarea{width:100%;padding:9px 10px;color:var(--text);background:#08131f;border:1px solid #304c68;border-radius:9px;outline:none}
.handoff-field textarea{min-height:94px;resize:vertical;font:inherit}
.handoff-field input:focus,.handoff-field textarea:focus{border-color:var(--accent)}
.handoff-link-grid{display:grid;grid-template-columns:1fr 1.5fr auto;gap:7px;align-items:end;margin-top:9px}
.handoff-link-grid label{margin-top:0}
.handoff-source-list{display:grid;gap:7px;margin-top:9px}
.handoff-source-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;align-items:center;padding:9px;border:1px solid #294159;border-radius:9px;background:#0b1825}
.handoff-source-row strong{display:block;color:#eef7ff;font-size:9px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.handoff-source-row span{display:block;margin-top:3px;color:#9fb4c9;font-size:8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.handoff-source-actions{display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end}
.handoff-source-actions button{padding:5px 7px;border:1px solid #34516b;border-radius:6px;background:#101f2e;color:#dcecff;cursor:pointer;font-size:8px}
.handoff-source-actions .remove{border-color:#71424b;background:#29191e;color:#ffc7cd}
.handoff-actions{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}
.handoff-btn{padding:8px 10px;border:1px solid #3b5b75;border-radius:8px;background:#102233;color:#dceeff;cursor:pointer;font-size:9px}
.handoff-btn:hover{border-color:#65d9ef}
.handoff-btn.primary{border-color:#4e9fbe;background:#173c52;color:#effcff}
.handoff-btn.chatgpt{border-color:#4a8060;background:#11291c;color:#d7ffe1}
.handoff-btn.warn{border-color:#71424b;background:#29191e;color:#ffc7cd}
.handoff-btn:disabled{opacity:.4;cursor:not-allowed}
.handoff-status{margin-top:9px;padding:8px 9px;border:1px dashed #35516b;border-radius:8px;background:#0b1723;color:#a9c3d8;font-size:8px;line-height:1.45}
.handoff-status.good{border-color:#47765a;background:#11261a;color:#c9f6d4}.handoff-status.warn{border-color:#816a35;background:#2b2410;color:#ffe4a1}
.handoff-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin-top:10px}
.handoff-stat{padding:9px;border:1px solid #2e4a63;border-radius:9px;background:#0b1825;min-width:0}
.handoff-stat strong{display:block;color:#eff8ff;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.handoff-stat span{display:block;margin-top:3px;color:#8fa8bd;font-size:8px;line-height:1.35}
.handoff-packet{width:100%;min-height:360px;margin-top:10px;padding:11px;color:#dcecff;background:#07121d;border:1px solid #304c68;border-radius:10px;resize:vertical;font:10px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;outline:none}
.handoff-plan{width:100%;min-height:260px;margin-top:9px;padding:11px;color:var(--text);background:#08131f;border:1px solid #304c68;border-radius:10px;resize:vertical;font:inherit;outline:none}
.handoff-packet:focus,.handoff-plan:focus{border-color:var(--accent)}
.handoff-output-section{margin-top:12px;padding-top:11px;border-top:1px solid #23394f}
.handoff-output-section:first-of-type{margin-top:0;padding-top:0;border-top:0}
.handoff-disclaimer{margin-top:9px;color:#7f96ab;font-size:8px;line-height:1.45}
@media(max-width:1040px){.handoff-layout{grid-template-columns:1fr}.handoff-stats{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media(max-width:700px){.handoff-head{display:block}.handoff-head .note{margin-top:8px}.handoff-fields,.handoff-link-grid,.handoff-stats{grid-template-columns:1fr}.handoff-source-row{grid-template-columns:1fr}.handoff-source-actions{justify-content:flex-start}}
'''.strip()
replace_once(
    ".gameplan-panel{grid-column:1/-1;padding:14px}",
    css + "\n\n.gameplan-panel{grid-column:1/-1;padding:14px}",
    "handoff CSS",
)
replace_once(
    "header,.left,.center,.right,.macro-panel,.scout-panel,.tendency-panel,.gameplan-builder,.gameplan-actions,.entry-actions,.gameplan-help,.modal-backdrop,footer{display:none!important}",
    "header,.left,.center,.right,.macro-panel,.scout-panel,.tendency-panel,.handoff-panel,.gameplan-builder,.gameplan-actions,.entry-actions,.gameplan-help,.modal-backdrop,footer{display:none!important}",
    "print handoff visibility",
)

# ---------- HTML ----------
panel = r'''
  <section class="panel handoff-panel" id="chatGptHandoffPanel">
    <div class="handoff-head">
      <div>
        <h2>ChatGPT Written Gameplan Handoff</h2>
        <div class="helptext">Create a link-first film packet for ChatGPT using public YouTube or Twitch film, your Scout Report, the Tendency Board, saved macros, and optional transcript or timestamp notes.</div>
      </div>
      <div class="note">This site does not upload or analyze video itself. It packages public film links and your scouting data so ChatGPT can produce a written defensive gameplan.</div>
    </div>

    <div class="handoff-layout">
      <div class="handoff-input">
        <h3>Film and Analysis Inputs</h3>
        <div class="handoff-fields">
          <div class="handoff-field">
            <label>Opponent</label>
            <input id="handoffOpponent" type="text" maxlength="100" placeholder="Opponent name">
          </div>
          <div class="handoff-field">
            <label>Week / Game</label>
            <input id="handoffWeek" type="text" maxlength="80" placeholder="Week 4, Playoffs, Rivalry Game…">
          </div>
        </div>

        <div class="handoff-link-grid">
          <div class="handoff-field"><label>Film Title</label><input id="handoffFilmTitle" type="text" maxlength="100" placeholder="Opponent vs Team — Week 3"></div>
          <div class="handoff-field"><label>YouTube or Twitch Link</label><input id="handoffFilmUrl" type="url" maxlength="500" placeholder="https://www.youtube.com/watch?v=…"></div>
          <button class="handoff-btn primary" id="addHandoffFilm" type="button">Add Film</button>
        </div>
        <div class="handoff-source-list" id="handoffSourceList"></div>

        <div class="handoff-field full">
          <label>Transcript or Play-by-Play Text <span style="color:#71889d">(optional)</span></label>
          <textarea id="handoffTranscript" maxlength="50000" placeholder="Paste a YouTube transcript, captions, play-by-play, or notes exported from another tool…"></textarea>
        </div>
        <div class="handoff-field full">
          <label>Timestamped Film Observations <span style="color:#71889d">(recommended)</span></label>
          <textarea id="handoffFilmNotes" maxlength="20000" placeholder="12:44 — 3rd &amp; Medium — Gun Trips — Mesh — slot motions across before snap…"></textarea>
        </div>
        <div class="handoff-field full">
          <label>Special Instructions for ChatGPT</label>
          <textarea id="handoffInstructions" maxlength="4000" placeholder="Prioritize stopping the slot seam, avoid heavy man coverage, give me an opening 15-call plan…"></textarea>
        </div>

        <div class="handoff-actions">
          <button class="handoff-btn" id="syncHandoffContext" type="button">Sync Opponent Context</button>
          <button class="handoff-btn warn" id="clearHandoff" type="button">New Blank Handoff</button>
        </div>
        <div class="handoff-status" id="handoffInputStatus"></div>
      </div>

      <div class="handoff-output">
        <div class="handoff-output-section">
          <div class="scout-saved-head"><strong>Generated ChatGPT Film Packet</strong><span class="call-sheet-count" id="handoffPacketSize">0 characters</span></div>
          <div class="handoff-stats" id="handoffStats"></div>
          <textarea class="handoff-packet" id="handoffPacketPreview" readonly></textarea>
          <div class="handoff-actions">
            <button class="handoff-btn primary" id="downloadHandoffPacket" type="button">Download Markdown Packet</button>
            <button class="handoff-btn" id="copyHandoffPacket" type="button">Copy Full Packet</button>
            <button class="handoff-btn" id="copyHandoffPrompt" type="button">Copy Master Prompt</button>
            <button class="handoff-btn chatgpt" id="openChatGpt" type="button">Open ChatGPT</button>
          </div>
          <div class="handoff-disclaimer">ChatGPT should use the public film links when accessible. If a platform blocks access, the packet explicitly requires it to rely on the included transcript, timestamp notes, Scout Report, and Tendency Board instead of inventing film observations.</div>
        </div>

        <div class="handoff-output-section">
          <div class="scout-saved-head"><strong>Returned Written Defensive Gameplan</strong><span class="call-sheet-count" id="handoffPlanStatus">Not saved</span></div>
          <textarea class="handoff-plan" id="handoffWrittenPlan" maxlength="60000" placeholder="Paste the written defensive gameplan returned by ChatGPT here so it stays with this opponent in the browser and in future backups."></textarea>
          <div class="handoff-actions">
            <button class="handoff-btn primary" id="saveHandoffPlan" type="button">Save Written Plan</button>
            <button class="handoff-btn" id="downloadHandoffPlan" type="button">Download Written Plan</button>
            <button class="handoff-btn" id="copyHandoffPlan" type="button">Copy Written Plan</button>
          </div>
        </div>
      </div>
    </div>
  </section>
'''.strip()
replace_once(
    '  <section class="panel gameplan-panel" id="gameplanPanel">',
    panel + '\n\n  <section class="panel gameplan-panel" id="gameplanPanel">',
    "handoff panel",
)

# ---------- JavaScript ----------
js = r'''
const CHATGPT_HANDOFF_STORAGE_KEY="cfb27-playbook-lab-v4-chatgpt-handoff";
const CHATGPT_HANDOFF_PROMPT=`You are acting as a defensive football gameplan analyst for College Football 27. Use the attached or pasted Opponent Film Analysis Packet.

FILM ACCESS RULES:
1. Attempt to open and analyze every public YouTube or Twitch URL listed in the packet when the link is accessible.
2. Do not claim that you watched, heard, transcribed, or verified film that you could not access.
3. When a link is blocked, expired, private, login-gated, or otherwise unavailable, explicitly identify that limitation and rely only on the included transcript, timestamped notes, Scout Report, Tendency Board, saved defensive macros, and current call sheet.
4. Separate verified observations from reasonable coaching inferences.
5. Do not invent exact frequencies, formations, concepts, player identities, or timestamps.

RETURN ONE WRITTEN DEFENSIVE GAMEPLAN WITH THESE SECTIONS:
1. Executive opponent profile
2. Film-access report listing which links were reviewed and which were unavailable
3. Personnel and formation tendencies
4. Core run concepts and fits
5. Core pass concepts and coverage stress points
6. Motion, tempo, protection, and danger-player alerts
7. Early-down plan
8. Third-down plan by short, medium, and long
9. Red-zone and goal-line plan
10. Mobile-QB, option, and RPO plan
11. Recommended primary macros from the packet
12. Recommended changeup macros from the packet
13. User-defender responsibilities and pre-snap adjustments
14. Opening 15 defensive calls or call families
15. Calls to avoid or limit
16. Unanswered questions and additional film needed

Use the exact macro names, formations, plays, strengths, and notes from the packet. If the available evidence is insufficient, state that clearly instead of guessing.`;

function emptyChatGptHandoff(){
  const scout=getScoutReport(),board=getTendencyBoard();
  return{opponent:TEAM_PLAYBOOKS[scout.opponent]?.name||TEAM_PLAYBOOKS[board.opponent]?.name||"",week:scout.week||board.week||"",sources:[],transcript:"",filmNotes:"",instructions:"",writtenPlan:"",planSavedAt:null,updatedAt:null};
}
function normalizeHandoff(raw){
  const base=emptyChatGptHandoff(),sources=(Array.isArray(raw?.sources)?raw.sources:[]).filter(source=>source&&typeof source.url==="string"&&isSupportedFilmUrl(source.url)).slice(-10).map((source,index)=>({id:String(source.id||`film-${index}-${Date.now()}`),title:typeof source.title==="string"&&source.title.trim()?source.title.trim().slice(0,100):`Film ${index+1}`,url:source.url.trim().slice(0,500)}));
  return{...base,...raw,opponent:typeof raw?.opponent==="string"?raw.opponent.slice(0,100):base.opponent,week:typeof raw?.week==="string"?raw.week.slice(0,80):base.week,sources,transcript:typeof raw?.transcript==="string"?raw.transcript.slice(0,50000):"",filmNotes:typeof raw?.filmNotes==="string"?raw.filmNotes.slice(0,20000):"",instructions:typeof raw?.instructions==="string"?raw.instructions.slice(0,4000):"",writtenPlan:typeof raw?.writtenPlan==="string"?raw.writtenPlan.slice(0,60000):"",planSavedAt:raw?.planSavedAt||null};
}
function getChatGptHandoff(){try{return normalizeHandoff(JSON.parse(localStorage.getItem(CHATGPT_HANDOFF_STORAGE_KEY)||"{}"))}catch{return emptyChatGptHandoff()}}
function storeChatGptHandoff(data){const normalized=normalizeHandoff(data);normalized.updatedAt=new Date().toISOString();localStorage.setItem(CHATGPT_HANDOFF_STORAGE_KEY,JSON.stringify(normalized));return normalized}
function isSupportedFilmUrl(value){
  try{const url=new URL(value),host=url.hostname.toLowerCase().replace(/^www\./,"");return url.protocol==="https:"&&(host==="youtube.com"||host.endsWith(".youtube.com")||host==="youtu.be"||host==="twitch.tv"||host.endsWith(".twitch.tv"))}catch{return false}
}
function filmPlatform(url){try{const host=new URL(url).hostname.toLowerCase();return host.includes("twitch")?"Twitch":"YouTube"}catch{return"Film"}}
function syncHandoffFromInputs(render=true){
  const handoff=getChatGptHandoff();handoff.opponent=el("handoffOpponent").value.trim();handoff.week=el("handoffWeek").value.trim();handoff.transcript=el("handoffTranscript").value;handoff.filmNotes=el("handoffFilmNotes").value;handoff.instructions=el("handoffInstructions").value;storeChatGptHandoff(handoff);if(render)renderChatGptHandoff();
}
function syncHandoffOpponentContext(){
  const handoff=getChatGptHandoff(),scout=getScoutReport(),board=getTendencyBoard();handoff.opponent=TEAM_PLAYBOOKS[scout.opponent]?.name||TEAM_PLAYBOOKS[board.opponent]?.name||handoff.opponent;handoff.week=scout.week||board.week||handoff.week;storeChatGptHandoff(handoff);renderChatGptHandoff();
}
function addHandoffFilm(){
  const title=el("handoffFilmTitle").value.trim(),url=el("handoffFilmUrl").value.trim();if(!isSupportedFilmUrl(url)){alert("Enter a public HTTPS YouTube or Twitch link.");return}const handoff=getChatGptHandoff();handoff.sources.push({id:`film-${Date.now()}-${Math.random().toString(36).slice(2,8)}`,title:title||`${filmPlatform(url)} Film ${handoff.sources.length+1}`,url});handoff.sources=handoff.sources.slice(-10);storeChatGptHandoff(handoff);el("handoffFilmTitle").value="";el("handoffFilmUrl").value="";renderChatGptHandoff();
}
function removeHandoffFilm(id){const handoff=getChatGptHandoff();handoff.sources=handoff.sources.filter(source=>source.id!==id);storeChatGptHandoff(handoff);renderChatGptHandoff()}
function handoffMacroSummary(macro,index){
  const assignments=Object.entries(macro.assignments||{}).map(([player,key])=>`${player}: ${ASSIGNMENT_LABELS[key]||key}`).join("; ");return `### Macro ${String(index+1).padStart(2,"0")} — ${macro.name}\n- Formation / Play: ${macro.formation} — ${macro.play}\n- Strength: ${(macro.strength||"left").toUpperCase()}\n- Type: ${(macro.playType||inferType(macro.play||"")).toUpperCase()}\n- Assignments: ${assignments||"No assignment snapshot available"}`;
}
function handoffTendencySummary(entry,index){
  const set=OFFENSIVE_SCOUT_SETS[entry.set],concept=OFFENSIVE_SCOUT_CONCEPTS[entry.concept],primary=tendencyMacro(entry.primaryMacroSlot),changeup=tendencyMacro(entry.changeupMacroSlot);return `### Tendency ${index+1} — ${entry.situation}\n- Frequency: ${entry.frequency}\n- Personnel: ${entry.personnel}\n- Set / Concept: ${set?.name||entry.set} — ${concept?.name||entry.concept}\n- Strength: ${entry.strength.toUpperCase()}\n- Primary Answer: ${primary?`Macro ${String(entry.primaryMacroSlot+1).padStart(2,"0")} — ${primary.name}`:"UNANSWERED"}\n- Changeup: ${changeup?`Macro ${String(entry.changeupMacroSlot+1).padStart(2,"0")} — ${changeup.name}`:"Unassigned"}\n- Alert: ${entry.alert||"None recorded"}\n- Coaching Note: ${entry.note||"None recorded"}`;
}
function buildChatGptPacket(){
  const handoff=getChatGptHandoff(),scout=getScoutReport(),board=getTendencyBoard(),macros=getMacros(),plan=getGameplan(),opponent=handoff.opponent||TEAM_PLAYBOOKS[scout.opponent]?.name||TEAM_PLAYBOOKS[board.opponent]?.name||"Opponent not specified",week=handoff.week||scout.week||board.week||"Game not specified";
  const sources=handoff.sources.length?handoff.sources.map((source,index)=>`${index+1}. [${source.title}](${source.url}) — ${filmPlatform(source.url)}`).join("\n"):"No public film links supplied.";
  const scoutPersonnel=(scout.personnel||[]).join(", ")||"Not recorded",scoutSet=OFFENSIVE_SCOUT_SETS[scout.set],scoutConcept=OFFENSIVE_SCOUT_CONCEPTS[scout.concept];
  const tendencyText=board.entries.length?board.entries.map(handoffTendencySummary).join("\n\n"):"No situation tendencies have been saved.";
  const macroText=macros.some(Boolean)?macros.map((macro,index)=>macro?handoffMacroSummary(macro,index):null).filter(Boolean).join("\n\n"):"No defensive macros have been saved.";
  const gameplanText=plan.entries.length?plan.entries.map((entry,index)=>`${index+1}. ${entry.situation} — ${entry.package.formation} — ${entry.package.play} — ${entry.source}${entry.note?` — ${entry.note}`:""}`).join("\n"):"No calls are currently on the Weekly Gameplan.";
  return `# CFB 27 Opponent Film Analysis Packet\n\n## Master Instructions\n${CHATGPT_HANDOFF_PROMPT}\n\n## Game Information\n- Opponent: ${opponent}\n- Week / Game: ${week}\n- Packet Generated: ${new Date().toLocaleString()}\n\n## Public Film Sources\n${sources}\n\n## Film Transcript / Play-by-Play\n${handoff.transcript.trim()||"No transcript supplied. Attempt the public links and use the timestamped notes below when direct film access is unavailable."}\n\n## Timestamped Film Observations\n${handoff.filmNotes.trim()||"No timestamped observations supplied."}\n\n## Special Instructions from the Coach\n${handoff.instructions.trim()||"No additional instructions supplied."}\n\n## Opponent Scout Report\n- Tempo: ${scout.tempo}\n- Run / Pass Tendency: ${scout.tendency}\n- Personnel: ${scoutPersonnel}\n- Mobile-QB Threat: ${scout.mobileQB?"Yes":"No"}\n- Frequent RPO / Option Stress: ${scout.rpo?"Yes":"No"}\n- Current Offensive Set: ${scoutSet?.name||scout.set}\n- Current Base Concept: ${scoutConcept?.name||scout.concept}\n- Favorite Concepts / Situational Tendencies: ${scout.concepts||"Not recorded"}\n- Protection, Matchup, and Gameplan Notes: ${scout.notes||"Not recorded"}\n\n## Situation-Based Tendency Board\n${tendencyText}\n\n## Available Defensive Macros\n${macroText}\n\n## Current Weekly Gameplan\n${gameplanText}\n\n## Required Final Reminder\nReturn the standardized written defensive gameplan requested in the Master Instructions. Clearly distinguish film-verified observations, coach-provided notes, and your own coaching inferences. Never claim to have reviewed an inaccessible link.`;
}
function handoffFileName(suffix="film-analysis-packet",extension="md"){const handoff=getChatGptHandoff(),base=(handoff.opponent||"opponent").replace(/[^a-z0-9]+/gi,"-").replace(/^-|-$/g,"").toLowerCase()||"opponent";return `${base}-${suffix}.${extension}`}
function downloadTextFile(filename,content,type="text/markdown"){const blob=new Blob([content],{type}),url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=filename;document.body.appendChild(a);a.click();a.remove();URL.revokeObjectURL(url)}
async function copyHandoffText(content,label){
  try{await navigator.clipboard.writeText(content);const status=el("handoffInputStatus");status.className="handoff-status good";status.textContent=`${label} copied to the clipboard.`}catch{const area=document.createElement("textarea");area.value=content;document.body.appendChild(area);area.select();document.execCommand("copy");area.remove();el("handoffInputStatus").textContent=`${label} copied to the clipboard.`}
}
function saveReturnedHandoffPlan(){const handoff=getChatGptHandoff();handoff.writtenPlan=el("handoffWrittenPlan").value.trim();handoff.planSavedAt=handoff.writtenPlan?new Date().toISOString():null;storeChatGptHandoff(handoff);renderChatGptHandoff()}
function clearChatGptHandoff(){const handoff=getChatGptHandoff();if((handoff.sources.length||handoff.transcript||handoff.filmNotes||handoff.instructions||handoff.writtenPlan)&&!confirm("Start a new blank ChatGPT gameplan handoff?"))return;storeChatGptHandoff(emptyChatGptHandoff());renderChatGptHandoff()}
function renderHandoffSources(handoff){
  const list=el("handoffSourceList");list.innerHTML="";if(!handoff.sources.length){const empty=document.createElement("div");empty.className="empty-state";empty.textContent="No film links added. Add one or more public YouTube or Twitch VODs above.";list.appendChild(empty);return}handoff.sources.forEach(source=>{const row=document.createElement("article");row.className="handoff-source-row";const main=document.createElement("div"),title=document.createElement("strong"),url=document.createElement("span");title.textContent=`${source.title} • ${filmPlatform(source.url)}`;url.textContent=source.url;main.append(title,url);const actions=document.createElement("div");actions.className="handoff-source-actions";const open=document.createElement("button");open.type="button";open.textContent="Open";open.onclick=()=>window.open(source.url,"_blank","noopener,noreferrer");const remove=document.createElement("button");remove.type="button";remove.className="remove";remove.textContent="Remove";remove.onclick=()=>removeHandoffFilm(source.id);actions.append(open,remove);row.append(main,actions);list.appendChild(row)})
}
function renderChatGptHandoff(){
  const handoff=getChatGptHandoff(),packet=buildChatGptPacket(),board=getTendencyBoard(),macros=getMacros(),plan=getGameplan(),bind=(id,value)=>{const node=el(id);if(document.activeElement!==node)node.value=value};bind("handoffOpponent",handoff.opponent);bind("handoffWeek",handoff.week);bind("handoffTranscript",handoff.transcript);bind("handoffFilmNotes",handoff.filmNotes);bind("handoffInstructions",handoff.instructions);bind("handoffWrittenPlan",handoff.writtenPlan);renderHandoffSources(handoff);el("handoffPacketPreview").value=packet;el("handoffPacketSize").textContent=`${packet.length.toLocaleString()} characters`;
  const stats=el("handoffStats");stats.innerHTML="";[[handoff.sources.length,"Film links"],[board.entries.length,"Tendencies"],[macros.filter(Boolean).length,"Saved macros"],[plan.entries.length,"Gameplan calls"]].forEach(([value,label])=>{const card=document.createElement("div");card.className="handoff-stat";const strong=document.createElement("strong"),span=document.createElement("span");strong.textContent=String(value);span.textContent=label;card.append(strong,span);stats.appendChild(card)});
  const status=el("handoffInputStatus"),hasFallback=!!(handoff.transcript.trim()||handoff.filmNotes.trim());status.className=`handoff-status ${handoff.sources.length&&!hasFallback?"warn":handoff.sources.length&&hasFallback?"good":""}`;status.textContent=!handoff.sources.length?"Add at least one public YouTube or Twitch film link. Transcript and timestamp notes remain optional but improve reliability.":hasFallback?"Link-first packet ready. Transcript or timestamp notes are included as a fallback when ChatGPT cannot access a VOD.":"Film links are ready. Add timestamp notes or a transcript when possible because direct VOD access is not guaranteed.";
  const planStatus=el("handoffPlanStatus");planStatus.textContent=handoff.planSavedAt?`Saved ${new Date(handoff.planSavedAt).toLocaleString()}`:handoff.writtenPlan?"Unsaved changes":"Not saved";["downloadHandoffPacket","copyHandoffPacket","copyHandoffPrompt"].forEach(id=>el(id).disabled=!packet.trim());el("downloadHandoffPlan").disabled=!handoff.writtenPlan.trim();el("copyHandoffPlan").disabled=!handoff.writtenPlan.trim();
}
'''.strip()
replace_once(
    "function getMacros(){",
    js + "\n\nfunction getMacros(){",
    "handoff JavaScript",
)
replace_once(
    "function renderAll(){\n  updateTypeBadge();renderField();renderPlayerGrid();renderAssignmentGroups();renderSummary();renderMapping();renderMacros();renderFavoriteControls();renderUndo();renderGameplan();renderScoutReport();renderTendencyBoard();\n}",
    "function renderAll(){\n  updateTypeBadge();renderField();renderPlayerGrid();renderAssignmentGroups();renderSummary();renderMapping();renderMacros();renderFavoriteControls();renderUndo();renderGameplan();renderScoutReport();renderTendencyBoard();renderChatGptHandoff();\n}",
    "render handoff",
)

bindings = r'''
["handoffOpponent","handoffWeek","handoffTranscript","handoffFilmNotes","handoffInstructions"].forEach(id=>el(id).addEventListener("input",()=>syncHandoffFromInputs(true)));
el("addHandoffFilm").onclick=addHandoffFilm;
el("handoffFilmUrl").addEventListener("keydown",event=>{if(event.key==="Enter"){event.preventDefault();addHandoffFilm()}});
el("syncHandoffContext").onclick=syncHandoffOpponentContext;
el("clearHandoff").onclick=clearChatGptHandoff;
el("downloadHandoffPacket").onclick=()=>downloadTextFile(handoffFileName(),buildChatGptPacket());
el("copyHandoffPacket").onclick=()=>copyHandoffText(buildChatGptPacket(),"Full gameplan packet");
el("copyHandoffPrompt").onclick=()=>copyHandoffText(CHATGPT_HANDOFF_PROMPT,"Master prompt");
el("openChatGpt").onclick=()=>window.open("https://chatgpt.com/","_blank","noopener,noreferrer");
el("saveHandoffPlan").onclick=saveReturnedHandoffPlan;
el("handoffWrittenPlan").addEventListener("input",()=>{const status=el("handoffPlanStatus");status.textContent=el("handoffWrittenPlan").value.trim()?"Unsaved changes":"Not saved"});
el("downloadHandoffPlan").onclick=()=>downloadTextFile(handoffFileName("written-defensive-gameplan","md"),getChatGptHandoff().writtenPlan);
el("copyHandoffPlan").onclick=()=>copyHandoffText(getChatGptHandoff().writtenPlan,"Written gameplan");
'''.strip()
replace_once(
    'function exportBackup(){',
    bindings + '\n\nfunction exportBackup(){',
    "handoff event bindings",
)

# ---------- Backup, reset, help, release ----------
replace_once(
    "    tendencyBoard:getTendencyBoard()\n  };",
    "    tendencyBoard:getTendencyBoard(),\n    chatGptHandoff:getChatGptHandoff()\n  };",
    "handoff backup export",
)
replace_once(
    'if(!confirm("Replace the saved macros, play maps, My Playbook list, weekly gameplan, team navigator, opponent scout report, and tendency board with this backup?"))return;',
    'if(!confirm("Replace the saved macros, play maps, My Playbook list, weekly gameplan, team navigator, opponent scout report, tendency board, and ChatGPT handoff with this backup?"))return;',
    "handoff backup import confirmation",
)
replace_once(
    "      storeTendencyBoard(data.tendencyBoard&&typeof data.tendencyBoard===\"object\"?data.tendencyBoard:emptyTendencyBoard());",
    "      storeTendencyBoard(data.tendencyBoard&&typeof data.tendencyBoard===\"object\"?data.tendencyBoard:emptyTendencyBoard());\n      storeChatGptHandoff(data.chatGptHandoff&&typeof data.chatGptHandoff===\"object\"?data.chatGptHandoff:emptyChatGptHandoff());",
    "handoff backup import storage",
)
replace_once(
    'const confirmation=prompt("This deletes every saved macro, play map, My Playbook selection, weekly gameplan, team navigator preference, opponent scout report, and tendency board in this browser. Type RESET to continue:");',
    'const confirmation=prompt("This deletes every saved macro, play map, My Playbook selection, weekly gameplan, team navigator preference, opponent scout report, tendency board, and ChatGPT handoff in this browser. Type RESET to continue:");',
    "handoff reset confirmation",
)
replace_once(
    '["cfb27-playbook-lab-v4-macros","cfb27-playbook-lab-v4-maps","cfb27-playbook-lab-v4-mybook",GAMEPLAN_STORAGE_KEY,TEAM_NAV_STORAGE_KEY,SCOUT_STORAGE_KEY,TENDENCY_STORAGE_KEY].forEach(key=>localStorage.removeItem(key));',
    '["cfb27-playbook-lab-v4-macros","cfb27-playbook-lab-v4-maps","cfb27-playbook-lab-v4-mybook",GAMEPLAN_STORAGE_KEY,TEAM_NAV_STORAGE_KEY,SCOUT_STORAGE_KEY,TENDENCY_STORAGE_KEY,CHATGPT_HANDOFF_STORAGE_KEY].forEach(key=>localStorage.removeItem(key));',
    "handoff reset storage",
)
replace_once(
    '<article class="help-card">\n              <h3>8. Build a weekly gameplan</h3>\n              <p>Select an opponent and situation, then add the current play, a saved macro, a tested scout-lab matchup, or a tendency-board answer. Reorder calls, reload them into the field, and print a clean call sheet.</p>\n            </article>',
    '<article class="help-card">\n              <h3>8. Create the ChatGPT handoff</h3>\n              <p>Add public YouTube or Twitch film links, optional transcript and timestamp notes, then download or copy the generated packet for ChatGPT. Paste the returned written plan back into the site to retain it.</p>\n            </article>\n            <article class="help-card">\n              <h3>9. Build a weekly gameplan</h3>\n              <p>Select an opponent and situation, then add the current play, a saved macro, a tested scout-lab matchup, or a tendency-board answer. Reorder calls, reload them into the field, and print a clean call sheet.</p>\n            </article>',
    "handoff help card",
)
replace_once(
    'Use <strong>Import Backup</strong> to transfer macros, play maps, My Playbook, the weekly gameplan, team navigator preferences, the opponent scout report, and the tendency board.',
    'Use <strong>Import Backup</strong> to transfer macros, play maps, My Playbook, the weekly gameplan, team navigator preferences, the opponent scout report, the tendency board, and the ChatGPT handoff.',
    "handoff backup help",
)
replace_once(
    '<div class="release-list">',
    '<div class="release-list">\n            <article class="release-item"><strong>ChatGPT written gameplan handoff</strong><span>Create a link-first film packet from public YouTube or Twitch VODs, transcripts, timestamp notes, the Scout Report, Tendency Board, macros, and call sheet; download or copy it for ChatGPT; and save the returned written gameplan back into the browser.</span></article>',
    "handoff release note",
)

INDEX.write_text(text, encoding="utf-8")
readme = README.read_text(encoding="utf-8")
marker = "- Situation-Based Opponent Tendency Board with situation/frequency/personnel organization, primary and changeup macro answers, unanswered-call and macro-overuse summaries, Scout Lab preview, Weekly Gameplan integration, local persistence, and backup support\n"
feature = "- ChatGPT Written Gameplan Handoff with link-first YouTube/Twitch film sources, optional transcript and timestamp notes, structured Markdown packet generation, prompt/full-packet copy, ChatGPT launch, returned-plan storage, and backup support\n"
if feature not in readme:
    if marker not in readme:
        raise SystemExit("README tendency-board marker missing")
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
new_ids=["chatGptHandoffPanel","handoffOpponent","handoffWeek","handoffFilmTitle","handoffFilmUrl","addHandoffFilm","handoffSourceList","handoffTranscript","handoffFilmNotes","handoffInstructions","syncHandoffContext","clearHandoff","handoffInputStatus","handoffPacketSize","handoffStats","handoffPacketPreview","downloadHandoffPacket","copyHandoffPacket","copyHandoffPrompt","openChatGpt","handoffPlanStatus","handoffWrittenPlan","saveHandoffPlan","downloadHandoffPlan","copyHandoffPlan"]
for item in new_ids:
    if parser.ids.count(item)!=1:raise SystemExit(f"Expected exactly one #{item}, found {parser.ids.count(item)}")
preserved=["libraryView","family","formation","play","field","playerGrid","assignmentGroups","macroList","saveMacro","overwriteMacro","clearMacros","scoutLabPanel","scoutOffensiveSet","scoutConcept","scoutMacro","scoutField","tendencyBoardPanel","tendencyList","gameplanPanel","gameplanCallSheet"]
for item in preserved:
    if parser.ids.count(item)!=1:raise SystemExit(f"Fundamental existing control #{item} changed unexpectedly")
required=["const CHATGPT_HANDOFF_STORAGE_KEY=","const CHATGPT_HANDOFF_PROMPT=","function buildChatGptPacket()","function renderChatGptHandoff()","chatGptHandoff:getChatGptHandoff()","CHATGPT_HANDOFF_STORAGE_KEY].forEach","https://chatgpt.com/"]
for item in required:
    if text.count(item)<1:raise SystemExit(f"Missing ChatGPT handoff integration marker: {item}")
script=re.search(r"<script>(.*)</script>",text,re.S)
if not script:raise SystemExit("Could not extract application JavaScript")
Path("/tmp/cfb27-chatgpt-handoff.js").write_text(script.group(1),encoding="utf-8")
print("ChatGPT written gameplan handoff patch validation passed.")
