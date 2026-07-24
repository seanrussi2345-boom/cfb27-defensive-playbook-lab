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


scout_css = r'''
.scout-panel{grid-column:1/-1;padding:14px}
.scout-head{display:flex;align-items:flex-start;justify-content:space-between;gap:14px}
.scout-head h2{margin-bottom:5px}
.scout-head .note{margin:0;max-width:590px}
.scout-layout{display:grid;grid-template-columns:390px minmax(0,1fr);gap:12px;margin-top:12px;align-items:start}
.scout-report,.scout-matchup{border:1px solid #294159;border-radius:12px;background:#08131f;padding:12px;min-width:0}
.scout-report h3,.scout-matchup h3{margin:0;color:#eaf7ff;font-size:12px}
.scout-fields{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.scout-field.full{grid-column:1/-1}
.scout-field label{margin-top:9px}
.scout-field input[type="text"],.scout-field select,.scout-field textarea{width:100%;padding:9px 10px;color:var(--text);background:#08131f;border:1px solid #304c68;border-radius:9px;outline:none}
.scout-field textarea{min-height:78px;resize:vertical;font:inherit}
.scout-field input:focus,.scout-field select:focus,.scout-field textarea:focus{border-color:var(--accent)}
.personnel-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px;margin-top:6px}
.personnel-option{display:flex;align-items:center;justify-content:center;gap:5px;padding:7px 5px;border:1px solid #304b66;border-radius:8px;background:#101e2c;color:#dcecff;font-size:9px;cursor:pointer}
.personnel-option input{margin:0}
.scout-checks{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:9px}
.scout-check{display:flex;align-items:center;gap:7px;padding:8px;border:1px solid #304b66;border-radius:8px;background:#101e2c;color:#dcecff;font-size:9px}
.scout-check input{margin:0}
.scout-actions{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}
.scout-btn{padding:8px 10px;border:1px solid #3b5b75;border-radius:8px;background:#102233;color:#dceeff;cursor:pointer;font-size:9px}
.scout-btn:hover{border-color:#65d9ef}
.scout-btn.primary{border-color:#4e9fbe;background:#173c52;color:#effcff}
.scout-btn.warn{border-color:#71424b;background:#29191e;color:#ffc7cd}
.scout-btn:disabled{opacity:.45;cursor:not-allowed}
.scout-control-grid{display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:8px;margin-top:9px}
.scout-field-wrap{margin-top:10px;min-height:470px;aspect-ratio:1.62/1;overflow:hidden;border:1px solid #315d43;border-radius:13px;background:#123e2a}
.scout-field-wrap svg{width:100%;height:100%}
.scout-summary{display:flex;gap:6px;flex-wrap:wrap;margin-top:9px}
.scout-summary span{padding:4px 7px;border:1px solid #34516b;border-radius:999px;background:#102033;color:#cce7f8;font-size:8px}
.scout-alerts{display:grid;gap:7px;margin-top:10px}
.scout-alert{padding:9px 10px;border:1px solid #36516b;border-radius:9px;background:#0b1723}
.scout-alert strong{display:block;color:#eaf7ff;font-size:9px}
.scout-alert span{display:block;margin-top:3px;color:#9fb4c9;font-size:8px;line-height:1.4}
.scout-alert.high{border-color:#7b434b;background:#29181d}
.scout-alert.medium{border-color:#816a35;background:#2b2410}
.scout-alert.good{border-color:#47765a;background:#11261a}
.scout-disclaimer{margin-top:9px;color:#7f96ab;font-size:8px;line-height:1.45}
.scout-saved{margin-top:12px;border-top:1px solid #23394f;padding-top:11px}
.scout-saved-head{display:flex;justify-content:space-between;gap:8px;align-items:center}
.scout-saved-head strong{font-size:10px;color:#eaf7ff}
.scout-saved-list{display:grid;gap:7px;margin-top:8px}
.scout-saved-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;align-items:center;padding:9px;border:1px solid #294159;border-radius:9px;background:#0b1825}
.scout-saved-row strong{display:block;color:#eef7ff;font-size:9px}
.scout-saved-row span{display:block;margin-top:3px;color:#9fb4c9;font-size:8px;line-height:1.35}
.scout-saved-actions{display:flex;gap:4px;flex-wrap:wrap;justify-content:flex-end}
.scout-saved-actions button{padding:5px 7px;border:1px solid #34516b;border-radius:6px;background:#101f2e;color:#dcecff;cursor:pointer;font-size:8px}
.scout-saved-actions .remove{border-color:#71424b;background:#29191e;color:#ffc7cd}
@media(max-width:1040px){.scout-layout{grid-template-columns:1fr}.scout-control-grid{grid-template-columns:1fr 1fr 1fr}}
@media(max-width:700px){.scout-head{display:block}.scout-head .note{margin-top:8px}.scout-fields,.scout-control-grid,.scout-checks{grid-template-columns:1fr}.personnel-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.scout-saved-row{grid-template-columns:1fr}.scout-saved-actions{justify-content:flex-start}}
'''.strip()
replace_once(
    ".gameplan-panel{grid-column:1/-1;padding:14px}",
    scout_css + "\n\n.gameplan-panel{grid-column:1/-1;padding:14px}",
    "scout CSS anchor",
)
replace_once(
    "header,.left,.center,.right,.macro-panel,.gameplan-builder,.gameplan-actions,.entry-actions,.gameplan-help,.modal-backdrop,footer{display:none!important}",
    "header,.left,.center,.right,.macro-panel,.scout-panel,.gameplan-builder,.gameplan-actions,.entry-actions,.gameplan-help,.modal-backdrop,footer{display:none!important}",
    "print visibility selector",
)

scout_html = r'''
  <section class="panel scout-panel" id="scoutLabPanel">
    <div class="scout-head">
      <div>
        <h2>Opponent Scout Report + Macro Matchup Lab</h2>
        <div class="helptext">Build one opponent report, then place a saved defensive macro over a generic offensive set to inspect structural stress before adding the call to the weekly gameplan.</div>
      </div>
      <div class="note">This module reads saved macro snapshots. It does not rewrite macro slots, play maps, live assignments, or the existing macro-builder field.</div>
    </div>

    <div class="scout-layout">
      <div class="scout-report">
        <h3>Opponent Scout Report</h3>
        <div class="scout-fields">
          <div class="scout-field">
            <label>Opponent</label>
            <select id="scoutOpponent"><option value="">No opponent selected</option></select>
          </div>
          <div class="scout-field">
            <label>Week / Game</label>
            <input id="scoutWeek" type="text" maxlength="80" placeholder="Week 1, Playoffs, Rivalry Game…">
          </div>
          <div class="scout-field">
            <label>Tempo</label>
            <select id="scoutTempo"><option>Balanced</option><option>Slow / Huddle</option><option>Multiple</option><option>No Huddle</option><option>Fast / Turbo</option></select>
          </div>
          <div class="scout-field">
            <label>Run / Pass Tendency</label>
            <select id="scoutTendency"><option>Balanced</option><option>Run Heavy</option><option>Pass Heavy</option><option>Early-Down Run</option><option>Early-Down Pass</option><option>Situational</option></select>
          </div>
          <div class="scout-field full">
            <label>Personnel Tendencies</label>
            <div class="personnel-grid" id="scoutPersonnelGrid">
              <label class="personnel-option"><input type="checkbox" value="10">10</label>
              <label class="personnel-option"><input type="checkbox" value="11">11</label>
              <label class="personnel-option"><input type="checkbox" value="12">12</label>
              <label class="personnel-option"><input type="checkbox" value="20">20</label>
              <label class="personnel-option"><input type="checkbox" value="21">21</label>
            </div>
          </div>
          <div class="scout-field full">
            <div class="scout-checks">
              <label class="scout-check"><input id="scoutMobileQB" type="checkbox"> Mobile-QB threat</label>
              <label class="scout-check"><input id="scoutRPO" type="checkbox"> Frequent RPO / option stress</label>
            </div>
          </div>
          <div class="scout-field full">
            <label>Favorite Concepts / Situational Tendencies</label>
            <textarea id="scoutConcepts" maxlength="500" placeholder="Slot seams, flood, mesh, counter, read option, red-zone bunch, third-down empty…"></textarea>
          </div>
          <div class="scout-field full">
            <label>Protection, Matchup, and Gameplan Notes</label>
            <textarea id="scoutNotes" maxlength="700" placeholder="Protection tells, best skill player, weak tackle, user responsibility, alerts…"></textarea>
          </div>
        </div>
        <div class="scout-actions">
          <button class="scout-btn warn" id="clearScoutReport" type="button">New Blank Scout</button>
        </div>
        <div class="scout-saved">
          <div class="scout-saved-head"><strong>Saved Macro Matchups</strong><span class="call-sheet-count" id="scoutSavedCount">0 saved</span></div>
          <div class="scout-saved-list" id="scoutSavedList"></div>
        </div>
      </div>

      <div class="scout-matchup">
        <h3>Macro vs Offensive Set</h3>
        <div class="scout-control-grid">
          <div class="scout-field">
            <label>Offensive Set</label>
            <select id="scoutOffensiveSet">
              <option value="gun2x2">Gun 2x2</option><option value="gunTrips">Gun Trips</option><option value="gunBunch">Gun Bunch</option>
              <option value="gunEmpty">Gun Empty</option><option value="tight2x2">Tight 2x2</option><option value="tripsTE">Trips TE</option>
              <option value="pistol">Pistol</option><option value="singleback">Singleback</option><option value="iform">I-Formation</option>
              <option value="splitBack">Split Back</option><option value="goalLine">Goal Line</option>
            </select>
          </div>
          <div class="scout-field">
            <label>Passing Strength</label>
            <select id="scoutStrength"><option value="left">Left</option><option value="right">Right</option></select>
          </div>
          <div class="scout-field">
            <label>Situation</label>
            <select id="scoutSituation"><option>Base Defense</option><option>1st &amp; 10</option><option>2nd &amp; Medium</option><option>3rd &amp; Short</option><option>3rd &amp; Medium</option><option>3rd &amp; Long</option><option>Red Zone</option><option>Goal Line</option><option>Two-Minute</option><option>Mobile QB</option><option>RPO</option><option>Bunch / Trips</option><option>Empty</option><option>Run Heavy</option><option>Custom</option></select>
          </div>
          <div class="scout-field full" style="grid-column:1/-1">
            <label>Saved Defensive Macro</label>
            <select id="scoutMacro"></select>
          </div>
        </div>
        <div class="scout-field-wrap"><svg id="scoutField" viewBox="0 0 1000 620" aria-label="Macro versus offensive set visualization"></svg></div>
        <div class="scout-summary" id="scoutMatchupSummary"></div>
        <div class="scout-alerts" id="scoutAlerts"></div>
        <div class="scout-disclaimer">Structural alerts are coaching prompts, not outcome predictions. Route combinations, motion, releases, blocking rules, personnel ratings, and user control can change the result.</div>
        <div class="scout-actions">
          <button class="scout-btn primary" id="saveScoutMatchup" type="button">Save Matchup to Scout</button>
          <button class="scout-btn" id="sendScoutToGameplan" type="button">Add to Weekly Gameplan</button>
          <button class="scout-btn" id="loadScoutInBuilder" type="button">Load Macro in Builder</button>
        </div>
      </div>
    </div>
  </section>
'''.strip()
replace_once(
    '  <section class="panel gameplan-panel" id="gameplanPanel">',
    scout_html + '\n\n  <section class="panel gameplan-panel" id="gameplanPanel">',
    "scout HTML insertion",
)

scout_js = r'''
const SCOUT_STORAGE_KEY="cfb27-playbook-lab-v4-scout";
const OFFENSIVE_SCOUT_SETS={
  gun2x2:{name:"Gun 2x2",personnel:"11",tags:["spread","seam"],players:[["X",70,548],["SL",255,548],["LT",400,565],["LG",450,565],["C",500,565],["RG",550,565],["RT",600,565],["SL",745,548],["Z",930,548],["QB",500,600],["RB",585,600]]},
  gunTrips:{name:"Gun Trips",personnel:"11",tags:["trips","seam"],players:[["X",70,548],["LT",400,565],["LG",450,565],["C",500,565],["RG",550,565],["RT",600,565],["Y",710,548],["SL",805,548],["Z",930,548],["QB",500,600],["RB",585,600]]},
  gunBunch:{name:"Gun Bunch",personnel:"11",tags:["bunch","traffic"],players:[["X",70,548],["LT",400,565],["LG",450,565],["C",500,565],["RG",550,565],["RT",600,565],["Y",765,548],["SL",825,530],["Z",890,555],["QB",500,600],["RB",585,600]]},
  gunEmpty:{name:"Gun Empty",personnel:"10",tags:["empty","spread","seam"],players:[["X",55,548],["SL",210,548],["LT",400,565],["LG",450,565],["C",500,565],["RG",550,565],["RT",600,565],["SL",790,548],["Z",945,548],["QB",500,600],["Y",690,548]]},
  tight2x2:{name:"Tight 2x2",personnel:"12",tags:["tight","seam","run"],players:[["X",270,548],["Y",350,548],["LT",410,565],["LG",455,565],["C",500,565],["RG",545,565],["RT",590,565],["Y",650,548],["Z",730,548],["QB",500,600],["RB",580,600]]},
  tripsTE:{name:"Trips TE",personnel:"11",tags:["trips","tight","seam"],players:[["X",70,548],["LT",400,565],["LG",450,565],["C",500,565],["RG",550,565],["RT",600,565],["Y",660,548],["SL",790,548],["Z",930,548],["QB",500,600],["RB",585,600]]},
  pistol:{name:"Pistol",personnel:"11",tags:["run","option"],players:[["X",70,548],["SL",250,548],["LT",400,565],["LG",450,565],["C",500,565],["RG",550,565],["RT",600,565],["Y",710,548],["Z",930,548],["QB",500,595],["RB",500,615]]},
  singleback:{name:"Singleback",personnel:"12",tags:["run","tight"],players:[["X",70,548],["Y",340,548],["LT",405,565],["LG",450,565],["C",500,565],["RG",550,565],["RT",595,565],["Y",660,548],["Z",930,548],["QB",500,592],["RB",500,615]]},
  iform:{name:"I-Formation",personnel:"21",tags:["run","heavy"],players:[["X",70,548],["Y",340,548],["LT",405,565],["LG",450,565],["C",500,565],["RG",550,565],["RT",595,565],["Z",930,548],["QB",500,590],["FB",500,605],["RB",500,618]]},
  splitBack:{name:"Split Back",personnel:"20",tags:["run","option"],players:[["X",70,548],["SL",250,548],["LT",400,565],["LG",450,565],["C",500,565],["RG",550,565],["RT",600,565],["Z",930,548],["QB",500,592],["RB",440,612],["RB",560,612]]},
  goalLine:{name:"Goal Line",personnel:"22",tags:["run","heavy","goal"],players:[["Y",300,548],["Y",350,548],["LT",405,565],["LG",450,565],["C",500,565],["RG",550,565],["RT",595,565],["Y",650,548],["QB",500,590],["FB",500,605],["RB",500,618]]}
};
let scoutPreviewPackage=null;
function emptyScoutReport(){return{opponent:"",week:"",tempo:"Balanced",tendency:"Balanced",personnel:["11"],mobileQB:false,rpo:false,concepts:"",notes:"",set:"gun2x2",strength:"right",situation:"Base Defense",macroSlot:null,matchups:[]}}
function normalizeScoutReport(raw){
  const base=emptyScoutReport(),validSets=new Set(Object.keys(OFFENSIVE_SCOUT_SETS)),validIds=new Set(Object.keys(TEAM_PLAYBOOKS));
  const matchups=Array.isArray(raw?.matchups)?raw.matchups.filter(item=>item&&item.package&&PLAY_DB[item.package.formation]?.includes(item.package.play)).slice(-20):[];
  return {...base,...raw,opponent:validIds.has(raw?.opponent)?raw.opponent:"",personnel:Array.isArray(raw?.personnel)?raw.personnel.filter(v=>["10","11","12","20","21"].includes(v)):[],set:validSets.has(raw?.set)?raw.set:"gun2x2",strength:raw?.strength==="left"?"left":"right",macroSlot:Number.isInteger(raw?.macroSlot)?raw.macroSlot:null,matchups};
}
function getScoutReport(){try{return normalizeScoutReport(JSON.parse(localStorage.getItem(SCOUT_STORAGE_KEY)||"{}"))}catch{return emptyScoutReport()}}
function storeScoutReport(report){const normalized=normalizeScoutReport(report);localStorage.setItem(SCOUT_STORAGE_KEY,JSON.stringify(normalized));return normalized}
function scoutMacroFor(report=getScoutReport()){const macros=getMacros();return Number.isInteger(report.macroSlot)?macros[report.macroSlot]||null:null}
function activeScoutPackage(report=getScoutReport()){return scoutPreviewPackage||scoutMacroFor(report)}
function scoutPackageSlot(report=getScoutReport()){return scoutPreviewPackage?.macroSlot??report.macroSlot}
function scoutDefenseCoords(ids){
  const map={CB1:[85,330],SCB:[250,365],SCB1:[230,365],SCB2:[770,365],CB2:[915,330],SS1:[285,220],FS1:[430,120],FS:[500,120],SS:[650,190],SS2:[715,220],SAM:[300,410],MIKE:[500,405],WILL:[700,410],JACK:[790,420],SUBLB1:[430,410],SUBLB2:[570,410],RLE:[350,485],LE:[350,485],RDT:[465,500],DT1:[465,500],NT:[500,500],DT2:[535,500],RRE:[650,485],RE:[650,485]};
  const result={},fallback={DB:[],S:[],LB:[],DL:[]};
  ids.forEach(id=>{if(map[id])result[id]=map[id];else if(/CB|SCB/.test(id))fallback.DB.push(id);else if(/FS|SS|SAF/.test(id))fallback.S.push(id);else if(/SAM|MIKE|WILL|JACK|LB/.test(id))fallback.LB.push(id);else fallback.DL.push(id)});
  const place=(list,y,left=180,right=820)=>list.forEach((id,index)=>{result[id]=[left+(right-left)*(index+1)/(list.length+1),y]});
  place(fallback.DB,340,80,920);place(fallback.S,190,260,740);place(fallback.LB,415,260,740);place(fallback.DL,495,320,680);return result;
}
function scoutGeometry(key,x,strength){
  const left=x<500,quarter=x<250?125:x<500?375:x<750?625:875,strongLeft=strength==="left";
  return {deepHalf:[left?270:730,65,210,76,"deep"],srcDeepHalfLeft:[270,65,210,76,"deep"],srcDeepHalfRight:[730,65,210,76,"deep"],deepThird:[x<335?155:x>665?845:500,80,125,72,"deep"],outsideThird:[left?155:845,80,125,72,"deep"],insideThird:[500,80,125,72,"deep"],deepQuarter:[quarter,80,92,70,"deep"],hookCurl:[Math.max(310,Math.min(690,x)),300,82,55,"under"],vertHook:[Math.max(350,Math.min(650,x)),245,76,68,"under"],threeRecHook:[strongLeft?420:580,285,92,58,"under"],middleRead:[500,220,95,76,"under"],srcHookLeft:[350,300,82,55,"under"],srcHookMid:[500,280,88,58,"under"],srcHookRight:[650,300,82,55,"under"],srcHookOuterLeft:[185,320,78,50,"under"],srcHookOuterRight:[815,320,78,50,"under"],srcFlatLeft:[105,385,82,46,"flat"],srcFlatRight:[895,385,82,46,"flat"],srcFlatInsideLeft:[195,350,82,48,"flat"],srcFlatInsideRight:[805,350,82,48,"flat"],hardFlat:[left?80:920,425,72,42,"flat"],cloudFlat:[left?105:895,365,82,52,"flat"],softSquat:[left?125:875,395,78,50,"flat"],flatTrap:[left?125:875,395,78,50,"flat"],curlFlat:[left?185:815,330,88,58,"flat"],seamFlat:[left?285:715,270,78,66,"flat"],quarterFlat:[left?235:765,305,83,58,"flat"],qbSpy:[500,465,58,36,"spy"],blitz:[500,565,0,0,"pressure"],qbContain:[left?350:650,550,0,0,"pressure"],manHidden:[x,0,0,0,"hidden"]}[key]||[x,0,0,0,"hidden"];
}
function drawScoutField(){
  const svg=el("scoutField"),report=getScoutReport(),set=OFFENSIVE_SCOUT_SETS[report.set],pkg=activeScoutPackage(report);svg.innerHTML="";
  const defs=svgEl("defs"),marker=svgEl("marker",{id:"scoutArrow",viewBox:"0 0 10 10",refX:"8",refY:"5",markerWidth:"6",markerHeight:"6",orient:"auto"});marker.appendChild(svgEl("path",{d:"M0 0 L10 5 L0 10 Z",fill:"#f4f8ff"}));defs.appendChild(marker);svg.appendChild(defs);
  svg.appendChild(svgEl("rect",{x:0,y:0,width:1000,height:620,fill:"#123e2a"}));for(let i=0;i<10;i++){svg.appendChild(svgEl("rect",{x:i*100,y:0,width:100,height:620,fill:i%2?"#184a32":"#123e2a"}));svg.appendChild(svgEl("line",{x1:i*100,y1:0,x2:i*100,y2:620,stroke:"rgba(255,255,255,.13)","stroke-width":2}))}svg.appendChild(svgEl("line",{x1:0,y1:525,x2:1000,y2:525,stroke:"#fff","stroke-width":4}));
  set.players.forEach(([name,x,y])=>{svg.appendChild(svgEl("circle",{cx:x,cy:y,r:name==="QB"?16:12,fill:"rgba(230,235,241,.78)",stroke:"#fff","stroke-width":2}));const t=svgEl("text",{x,y:y+3,"text-anchor":"middle",fill:"#071018","font-size":name==="QB"?9:7,"font-weight":900});t.textContent=name;svg.appendChild(t)});
  if(!pkg){const t=svgEl("text",{x:500,y:260,"text-anchor":"middle",fill:"#d8e8f5","font-size":20,"font-weight":800});t.textContent="Save a macro, then select it here";svg.appendChild(t);return}
  const assignments=pkg.assignments||{},ids=Object.keys(assignments),coords=scoutDefenseCoords(ids),colors={deep:["rgba(101,217,239,.22)","#65d9ef"],under:["rgba(126,227,154,.22)","#7ee39a"],flat:["rgba(255,214,111,.23)","#ffd66f"],spy:["rgba(193,155,255,.24)","#c19bff"],pressure:["rgba(255,173,100,.12)","#ffad64"],hidden:["rgba(127,145,164,.06)","#7f91a4"]};
  ids.forEach(id=>{const [x,y]=coords[id],key=assignments[id],[tx,ty,rx,ry,type]=scoutGeometry(key,x,report.strength),[,stroke]=colors[type];if(type==="deep"||type==="under"||type==="flat"||type==="spy"){svg.appendChild(svgEl("ellipse",{cx:tx,cy:ty,rx,ry,fill:colors[type][0],stroke,"stroke-width":2}));svg.appendChild(svgEl("line",{x1:x,y1:y,x2:tx,y2:ty,stroke,"stroke-width":2,"stroke-dasharray":"7 5","marker-end":"url(#scoutArrow)"}))}else if(type==="pressure"){svg.appendChild(svgEl("line",{x1:x,y1:y,x2:tx,y2:ty,stroke,"stroke-width":3,"marker-end":"url(#scoutArrow)"}))}svg.appendChild(svgEl("circle",{cx:x,cy:y,r:16,fill:"#0d2434",stroke,"stroke-width":3}));const label=svgEl("text",{x,y:y+3,"text-anchor":"middle",fill:"#fff","font-size":8,"font-weight":900});label.textContent=id;svg.appendChild(label);if(type==="hidden"){const m=svgEl("text",{x,y:y-22,"text-anchor":"middle",fill:"#dce6ef","font-size":8,"font-weight":900});m.textContent="MAN";svg.appendChild(m)}});
}
function scoutAlerts(report=getScoutReport(),pkg=activeScoutPackage(report)){
  if(!pkg)return[{level:"medium",title:"No saved macro selected",detail:"Build and save a macro in the existing macro builder, then select that slot for the matchup lab."}];
  const set=OFFENSIVE_SCOUT_SETS[report.set],a=pkg.assignments||{},entries=Object.entries(a),values=entries.map(([,v])=>v),count=re=>values.filter(v=>re.test(v)).length,alerts=[];
  const blitz=count(/blitz/),contain=count(/qbContain/),spy=count(/qbSpy/),seam=count(/seamFlat|quarterFlat|vertHook|middleRead|threeRecHook/),flat=count(/Flat|curlFlat|hardFlat|cloudFlat|softSquat|flatTrap/),man=count(/manHidden/),box=entries.filter(([id,v])=>/SAM|MIKE|WILL|JACK|LB|RLE|RRE|RDT|NT|DT|LE|RE/.test(id)&&!/deep|outsideThird|insideThird|Flat/.test(v)).length;
  if(report.mobileQB&&!contain&&!spy)alerts.push({level:"high",title:"No dedicated contain or spy",detail:"The scout marks a mobile quarterback, but this macro snapshot has no QB contain or spy responsibility."});
  if(report.mobileQB&&(contain||spy))alerts.push({level:"good",title:"Quarterback control present",detail:`This macro includes ${contain} contain and ${spy} spy responsibility${contain+spy===1?"":"ies"}.`});
  if(set.tags.includes("empty")&&man>=4)alerts.push({level:"medium",title:"Empty formation man-match stress",detail:"Verify cross-field matches, slot leverage, and traffic rules before relying on this call against empty."});
  if(set.tags.includes("empty")&&blitz>=5)alerts.push({level:"high",title:"Pressure leaves immediate hot answers",detail:"Five or more rushers against empty can expose quick seams, speed outs, and back-side hot throws."});
  if(set.tags.includes("bunch")&&flat<2)alerts.push({level:"high",title:"Bunch leverage stress",detail:"The macro shows limited flat/curl-flat structure. Confirm banjo, point, and outside-release responsibilities."});
  if(set.tags.includes("trips")&&seam<2)alerts.push({level:"medium",title:"Trips seam stress",detail:"The trips surface has fewer than two seam/middle carry responsibilities in the saved snapshot."});
  if(set.tags.includes("seam")&&seam<2)alerts.push({level:"medium",title:"Interior vertical window",detail:"The offensive shell threatens both seams while the macro shows limited vertical-hook or seam-flat support."});
  if(set.tags.includes("run")&&box<6)alerts.push({level:"high",title:"Light structural box",detail:`Only ${box} front/box defenders remain structurally available against a run-oriented shell.`});
  if(report.rpo&&blitz>=5)alerts.push({level:"medium",title:"RPO conflict behind pressure",detail:"Heavy pressure can widen the conflict defender and create an immediate glance, bubble, or replace throw."});
  if(blitz>=5)alerts.push({level:"medium",title:"Screen and hot-outlet exposure",detail:`The saved macro sends ${blitz} rushers. Verify the screen retrace and immediate outlet answer.`});
  if(!alerts.some(item=>item.level==="high"))alerts.push({level:"good",title:"No major structural red flag detected",detail:"The shell still requires in-game verification for motion, releases, protection, personnel ratings, and user control."});
  return alerts;
}
function populateScoutMacros(report=getScoutReport()){
  const select=el("scoutMacro"),macros=getMacros(),current=report.macroSlot;select.innerHTML="";const available=[];macros.forEach((macro,index)=>{if(!macro)return;available.push(index);const option=document.createElement("option");option.value=String(index);option.textContent=`${String(index+1).padStart(2,"0")} — ${macro.name} | ${macro.formation} — ${macro.play}`;select.appendChild(option)});if(!available.length){const option=document.createElement("option");option.value="";option.textContent="No saved macros available";select.appendChild(option);select.disabled=true;report.macroSlot=null;storeScoutReport(report)}else{select.disabled=false;if(!available.includes(current)){report.macroSlot=available[0];storeScoutReport(report)}select.value=String(report.macroSlot)}
}
function renderScoutSaved(report=getScoutReport()){
  const list=el("scoutSavedList");list.innerHTML="";el("scoutSavedCount").textContent=`${report.matchups.length} saved`;if(!report.matchups.length){const empty=document.createElement("div");empty.className="empty-state";empty.textContent="No tested macro matchups saved yet.";list.appendChild(empty);return}report.matchups.slice().reverse().forEach(item=>{const row=document.createElement("article");row.className="scout-saved-row";const main=document.createElement("div"),title=document.createElement("strong"),meta=document.createElement("span");title.textContent=`${OFFENSIVE_SCOUT_SETS[item.set]?.name||item.set} — ${item.package.name||item.package.play}`;meta.textContent=`${item.situation} • ${item.package.formation} — ${item.package.play} • ${item.alertCount} alert${item.alertCount===1?"":"s"}`;main.append(title,meta);const actions=document.createElement("div");actions.className="scout-saved-actions";const preview=document.createElement("button");preview.textContent="Preview";preview.onclick=()=>{scoutPreviewPackage={...clonePackage(item.package),macroSlot:item.macroSlot};const r=getScoutReport();r.set=item.set;r.strength=item.strength;r.situation=item.situation;storeScoutReport(r);renderScoutReport()};const gameplan=document.createElement("button");gameplan.textContent="Gameplan";gameplan.onclick=()=>sendScoutPackageToGameplan(item.package,item.macroSlot,`Saved Scout: ${OFFENSIVE_SCOUT_SETS[item.set]?.name||item.set}`,item.situation);const remove=document.createElement("button");remove.className="remove";remove.textContent="Remove";remove.onclick=()=>{const r=getScoutReport();r.matchups=r.matchups.filter(saved=>saved.id!==item.id);storeScoutReport(r);renderScoutReport()};actions.append(preview,gameplan,remove);row.append(main,actions);list.appendChild(row)})
}
function renderScoutReport(){
  const report=getScoutReport(),set=OFFENSIVE_SCOUT_SETS[report.set];populateScoutMacros(report);const bind=(id,value)=>{const node=el(id);if(document.activeElement!==node)node.value=value};bind("scoutOpponent",report.opponent);bind("scoutWeek",report.week);bind("scoutTempo",report.tempo);bind("scoutTendency",report.tendency);bind("scoutConcepts",report.concepts);bind("scoutNotes",report.notes);bind("scoutOffensiveSet",report.set);bind("scoutStrength",report.strength);bind("scoutSituation",report.situation);el("scoutMobileQB").checked=report.mobileQB;el("scoutRPO").checked=report.rpo;document.querySelectorAll('#scoutPersonnelGrid input[type="checkbox"]').forEach(box=>box.checked=report.personnel.includes(box.value));drawScoutField();const pkg=activeScoutPackage(report),alerts=scoutAlerts(report,pkg),summary=el("scoutMatchupSummary");summary.innerHTML="";[set.name,`Personnel ${set.personnel}`,pkg?`${pkg.formation} — ${pkg.play}`:"No macro",`Strength ${report.strength.toUpperCase()}`].forEach(value=>{const span=document.createElement("span");span.textContent=value;summary.appendChild(span)});const alertWrap=el("scoutAlerts");alertWrap.innerHTML="";alerts.forEach(item=>{const card=document.createElement("div");card.className=`scout-alert ${item.level}`;const strong=document.createElement("strong"),detail=document.createElement("span");strong.textContent=item.title;detail.textContent=item.detail;card.append(strong,detail);alertWrap.appendChild(card)});const disabled=!pkg;["saveScoutMatchup","sendScoutToGameplan","loadScoutInBuilder"].forEach(id=>el(id).disabled=disabled);renderScoutSaved(report)
}
function updateScoutReportFromInputs(){const report=getScoutReport();report.opponent=el("scoutOpponent").value;report.week=el("scoutWeek").value;report.tempo=el("scoutTempo").value;report.tendency=el("scoutTendency").value;report.personnel=[...document.querySelectorAll('#scoutPersonnelGrid input[type="checkbox"]:checked')].map(box=>box.value);report.mobileQB=el("scoutMobileQB").checked;report.rpo=el("scoutRPO").checked;report.concepts=el("scoutConcepts").value;report.notes=el("scoutNotes").value;report.set=el("scoutOffensiveSet").value;report.strength=el("scoutStrength").value;report.situation=el("scoutSituation").value;report.macroSlot=el("scoutMacro").value===""?null:Number(el("scoutMacro").value);scoutPreviewPackage=null;storeScoutReport(report);renderScoutReport()}
function saveScoutMatchup(){const report=getScoutReport(),pkg=activeScoutPackage(report);if(!pkg)return;const alerts=scoutAlerts(report,pkg);report.matchups.push({id:`scout-${Date.now()}-${Math.random().toString(36).slice(2,8)}`,set:report.set,strength:report.strength,situation:report.situation,macroSlot:scoutPackageSlot(report),package:clonePackage(pkg),alertCount:alerts.filter(item=>item.level!=="good").length,savedAt:new Date().toISOString()});report.matchups=report.matchups.slice(-20);storeScoutReport(report);renderScoutReport()}
function sendScoutPackageToGameplan(pkg=activeScoutPackage(),macroSlot=scoutPackageSlot(),source="Opponent Scout Lab",situation=getScoutReport().situation){if(!pkg)return;const report=getScoutReport(),plan=getGameplan();if(report.opponent)plan.opponent=report.opponent;if(report.week)plan.week=report.week;const set=OFFENSIVE_SCOUT_SETS[report.set];plan.entries.push({id:`call-${Date.now()}-${Math.random().toString(36).slice(2,8)}`,situation,note:[`vs ${set.name}`,report.concepts.trim()].filter(Boolean).join(" • "),source,macroSlot:Number.isInteger(macroSlot)?macroSlot:null,package:clonePackage(pkg)});storeGameplan(plan);renderGameplan();el("gameplanPanel")?.scrollIntoView({behavior:"smooth",block:"start"})}
function clearScoutReport(){const report=getScoutReport();if((report.notes||report.concepts||report.matchups.length)&&!confirm("Start a new blank opponent scout report?"))return;scoutPreviewPackage=null;storeScoutReport(emptyScoutReport());renderScoutReport()}
'''.strip()
replace_once("function getMacros(){", scout_js + "\n\nfunction getMacros(){", "scout JavaScript insertion")
replace_once(
    "updateTypeBadge();renderField();renderPlayerGrid();renderAssignmentGroups();renderSummary();renderMapping();renderMacros();renderFavoriteControls();renderUndo();renderGameplan();",
    "updateTypeBadge();renderField();renderPlayerGrid();renderAssignmentGroups();renderSummary();renderMapping();renderMacros();renderFavoriteControls();renderUndo();renderGameplan();renderScoutReport();",
    "renderAll integration",
)

scout_handlers = r'''
["scoutOpponent","scoutWeek","scoutTempo","scoutTendency","scoutConcepts","scoutNotes","scoutOffensiveSet","scoutStrength","scoutSituation","scoutMacro","scoutMobileQB","scoutRPO"].forEach(id=>{
  const node=el(id);node.addEventListener(node.tagName==="TEXTAREA"||node.type==="text"?"input":"change",updateScoutReportFromInputs);
});
document.querySelectorAll('#scoutPersonnelGrid input[type="checkbox"]').forEach(box=>box.addEventListener("change",updateScoutReportFromInputs));
el("saveScoutMatchup").onclick=saveScoutMatchup;
el("sendScoutToGameplan").onclick=()=>sendScoutPackageToGameplan();
el("loadScoutInBuilder").onclick=()=>{const pkg=activeScoutPackage();if(pkg)loadPlayPackage(pkg,scoutPackageSlot())};
el("clearScoutReport").onclick=clearScoutReport;
'''.strip()
replace_once("function exportBackup(){", scout_handlers + "\n\nfunction exportBackup(){", "scout event handlers")
replace_once(
    "    teamNavigator:getTeamNavigator()\n  };",
    "    teamNavigator:getTeamNavigator(),\n    scoutReport:getScoutReport()\n  };",
    "backup export scout data",
)
replace_once(
    'if(!confirm("Replace the saved macros, play maps, My Playbook list, weekly gameplan, and team navigator with this backup?"))return;',
    'if(!confirm("Replace the saved macros, play maps, My Playbook list, weekly gameplan, team navigator, and opponent scout report with this backup?"))return;',
    "backup confirmation",
)
replace_once(
    '      storeTeamNavigator(data.teamNavigator&&typeof data.teamNavigator==="object"?data.teamNavigator:emptyTeamNavigator());',
    '      storeTeamNavigator(data.teamNavigator&&typeof data.teamNavigator==="object"?data.teamNavigator:emptyTeamNavigator());\n      storeScoutReport(data.scoutReport&&typeof data.scoutReport==="object"?data.scoutReport:emptyScoutReport());',
    "backup import scout data",
)
replace_once(
    "This deletes every saved macro, play map, My Playbook selection, weekly gameplan, and team navigator preference in this browser. Type RESET to continue:",
    "This deletes every saved macro, play map, My Playbook selection, weekly gameplan, team navigator preference, and opponent scout report in this browser. Type RESET to continue:",
    "reset confirmation scout text",
)
replace_once(
    '["cfb27-playbook-lab-v4-macros","cfb27-playbook-lab-v4-maps","cfb27-playbook-lab-v4-mybook",GAMEPLAN_STORAGE_KEY,TEAM_NAV_STORAGE_KEY]',
    '["cfb27-playbook-lab-v4-macros","cfb27-playbook-lab-v4-maps","cfb27-playbook-lab-v4-mybook",GAMEPLAN_STORAGE_KEY,TEAM_NAV_STORAGE_KEY,SCOUT_STORAGE_KEY]',
    "reset scout storage key",
)
replace_once(
    'sortedTeamEntries.forEach(([id,book])=>{\n  const option=document.createElement("option");option.value=id;option.textContent=book.name||id;el("gameplanOpponent").appendChild(option);\n});',
    'sortedTeamEntries.forEach(([id,book])=>{\n  const option=document.createElement("option");option.value=id;option.textContent=book.name||id;el("gameplanOpponent").appendChild(option);\n  const scoutOption=document.createElement("option");scoutOption.value=id;scoutOption.textContent=book.name||id;el("scoutOpponent").appendChild(scoutOption);\n});',
    "scout opponent initialization",
)

old_help = '''            <article class="help-card">
              <h3>6. Build a weekly gameplan</h3>
              <p>Select an opponent and situation, then add the current play or a saved macro. Reorder calls, reload them into the field, and print a clean call sheet.</p>
            </article>'''
new_help = '''            <article class="help-card">
              <h3>6. Scout the opponent</h3>
              <p>Record personnel, tempo, concepts, mobile-QB and RPO tendencies, then test a saved macro against a generic offensive set without changing the macro slot.</p>
            </article>
            <article class="help-card">
              <h3>7. Build a weekly gameplan</h3>
              <p>Select an opponent and situation, then add the current play, a saved macro, or a tested scout-lab matchup. Reorder calls, reload them into the field, and print a clean call sheet.</p>
            </article>'''
replace_once(old_help, new_help, "scout help card")
replace_once(
    "Use <strong>Import Backup</strong> to transfer macros, play maps, My Playbook, the weekly gameplan, and team navigator preferences.",
    "Use <strong>Import Backup</strong> to transfer macros, play maps, My Playbook, the weekly gameplan, team navigator preferences, and the opponent scout report.",
    "help backup scout text",
)
replace_once(
    '<article class="release-item"><strong>Searchable team playbook navigator</strong>',
    '<article class="release-item"><strong>Opponent scout report and macro matchup lab</strong><span>Track offensive tendencies, place saved macro assignments over generic offensive sets, flag structural stress, save tested matchups, and send them to the weekly gameplan without changing macro slots.</span></article>\n            <article class="release-item"><strong>Searchable team playbook navigator</strong>',
    "scout release note",
)

INDEX.write_text(text, encoding="utf-8")
readme = README.read_text(encoding="utf-8")
marker = "- Weekly Gameplan Builder with opponent selection, situation-based calls, current-play and macro capture, reordering, reload, local persistence, backup support, and a print-friendly Call-Sheet View\n"
feature = "- Opponent Scout Report and Macro Matchup Lab with offensive tendency tracking, generic offensive-set shells, read-only saved-macro visualization, structural coaching alerts, saved matchup notes, weekly-gameplan integration, local persistence, and backup support\n"
if feature not in readme:
    if marker not in readme:
        raise SystemExit("README weekly gameplan marker missing")
    readme = readme.replace(marker, marker + feature, 1)
README.write_text(readme, encoding="utf-8")


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key == "id" and value:
                self.ids.append(value)


parser = IdCollector()
parser.feed(text)
new_ids = ["scoutLabPanel","scoutOpponent","scoutWeek","scoutTempo","scoutTendency","scoutMobileQB","scoutRPO","scoutConcepts","scoutNotes","scoutOffensiveSet","scoutStrength","scoutSituation","scoutMacro","scoutField","scoutAlerts","scoutSavedList","saveScoutMatchup","sendScoutToGameplan","loadScoutInBuilder","clearScoutReport"]
for item in new_ids:
    if parser.ids.count(item) != 1:
        raise SystemExit(f"Expected exactly one #{item}, found {parser.ids.count(item)}")
preserved = ["libraryView","family","formation","play","field","playerGrid","assignmentGroups","macroList","saveMacro","overwriteMacro","clearMacros","gameplanPanel","gameplanCallSheet"]
for item in preserved:
    if parser.ids.count(item) != 1:
        raise SystemExit(f"Fundamental macro-builder control #{item} changed unexpectedly")
required = ["const SCOUT_STORAGE_KEY=","function renderScoutReport","function drawScoutField","scoutReport:getScoutReport()","storeScoutReport(data.scoutReport","renderGameplan();renderScoutReport();"]
for item in required:
    if text.count(item) != 1:
        raise SystemExit(f"Expected one scout integration marker: {item}")
script = re.search(r"<script>(.*)</script>", text, re.S)
if not script:
    raise SystemExit("Could not extract application JavaScript")
Path("/tmp/cfb27-scout-lab.js").write_text(script.group(1), encoding="utf-8")
print("Opponent Scout Report and Macro Matchup Lab patch validation passed.")
