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


def sub_once(pattern: str, replacement: str, label: str) -> None:
    global text
    compiled = re.compile(pattern, re.S)
    matches = list(compiled.finditer(text))
    if len(matches) != 1:
        raise SystemExit(f"{label}: expected one source block, found {len(matches)}")
    text = compiled.sub(lambda _: replacement, text, count=1)


# Layout and visual legend for the offensive concept layer.
replace_once(
    ".scout-control-grid{display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:8px;margin-top:9px}",
    ".scout-control-grid{display:grid;grid-template-columns:1.15fr 1.15fr .8fr .9fr;gap:8px;margin-top:9px}",
    "scout control grid",
)
replace_once(
    ".scout-field-wrap svg{width:100%;height:100%}",
    ".scout-field-wrap svg{width:100%;height:100%}\n.scout-concept-note{margin-top:8px;padding:8px 9px;border:1px dashed #35516b;border-radius:8px;background:#0b1723;color:#a9c3d8;font-size:9px;line-height:1.45}\n.scout-route-legend{display:flex;gap:12px;flex-wrap:wrap;margin-top:8px;color:#9fb4c9;font-size:8px}\n.scout-route-legend span{display:flex;align-items:center;gap:5px}\n.scout-route-legend i{display:block;width:20px;height:3px;border-radius:3px}\n.scout-route-legend .pass{background:#ff96d7}.scout-route-legend .run{background:#f4f8ff}.scout-route-legend .read{background:#ffd66f}.scout-route-legend .block{background:#9fb4c9}",
    "concept CSS",
)
replace_once(
    "@media(max-width:1040px){.scout-layout{grid-template-columns:1fr}.scout-control-grid{grid-template-columns:1fr 1fr 1fr}}",
    "@media(max-width:1040px){.scout-layout{grid-template-columns:1fr}.scout-control-grid{grid-template-columns:1fr 1fr}}",
    "scout responsive grid",
)

# Add the offensive concept selector without disturbing the macro selector.
replace_once(
    "        <h3>Macro vs Offensive Set</h3>",
    "        <h3>Macro vs Offensive Set + Concept</h3>",
    "scout matchup heading",
)
concept_field = '''          <div class="scout-field">
            <label>Base Offensive Concept</label>
            <select id="scoutConcept"></select>
          </div>
'''
replace_once(
    '''          <div class="scout-field">
            <label>Passing Strength</label>
            <select id="scoutStrength"><option value="left">Left</option><option value="right">Right</option></select>
          </div>''',
    concept_field + '''          <div class="scout-field">
            <label>Passing Strength</label>
            <select id="scoutStrength"><option value="left">Left</option><option value="right">Right</option></select>
          </div>''',
    "offensive concept selector",
)
replace_once(
    '''        </div>
        <div class="scout-field-wrap"><svg id="scoutField" viewBox="0 0 1000 620" aria-label="Macro versus offensive set visualization"></svg></div>
        <div class="scout-summary" id="scoutMatchupSummary"></div>''',
    '''        </div>
        <div class="scout-concept-note" id="scoutConceptDescription"></div>
        <div class="scout-field-wrap"><svg id="scoutField" viewBox="0 0 1000 620" aria-label="Defensive macro versus offensive set and concept visualization"></svg></div>
        <div class="scout-route-legend"><span><i class="pass"></i>Pass route</span><span><i class="run"></i>Run track</span><span><i class="read"></i>Read / option path</span><span><i class="block"></i>Lead / screen block</span></div>
        <div class="scout-summary" id="scoutMatchupSummary"></div>''',
    "concept description and legend",
)

concept_data = r'''
const OFFENSIVE_SCOUT_CONCEPTS={
  fourVerticals:{name:"Four Verticals",category:"Pass",tags:["vertical","seam"],description:"Four receivers push vertically to stress seams, deep halves, thirds, quarters, and middle-carry rules."},
  mesh:{name:"Mesh",category:"Pass",tags:["cross","traffic","quick"],description:"Two shallow crossers create traffic with an outside clear-out and an intermediate settle or corner route."},
  shallowCross:{name:"Shallow Cross",category:"Pass",tags:["cross","levels"],description:"A shallow crosser works underneath an intermediate dig with vertical clear-out routes."},
  drive:{name:"Drive",category:"Pass",tags:["cross","levels"],description:"A shallow route and a deeper dig attack the same underneath defenders at two levels."},
  levels:{name:"Levels",category:"Pass",tags:["levels","zone"],description:"Multiple in-breaking routes settle at staggered depths against hook and curl defenders."},
  dagger:{name:"Dagger",category:"Pass",tags:["vertical","dig","shot"],description:"An inside vertical clears the middle for a deep dig from the outside receiver."},
  mills:{name:"Mills / Post-Dig",category:"Pass",tags:["post","dig","shot"],description:"A post and dig create a high-low conflict on the middle safety and inside zone defenders."},
  flood:{name:"Flood",category:"Pass",tags:["flood","threeLevel"],description:"A vertical, intermediate out/corner, and flat route stretch one sideline at three depths."},
  sail:{name:"Sail",category:"Pass",tags:["flood","threeLevel"],description:"A clear-out, sail route, and flat control the deep-third, curl-flat, and flat defender on one side."},
  smash:{name:"Smash",category:"Pass",tags:["smash","highLow"],description:"A hitch or stop sits beneath a corner route to high-low the flat defender and deep half."},
  stick:{name:"Stick",category:"Pass",tags:["quick","spacing"],description:"A stick route, flat route, and vertical clear-out create a fast triangle read."},
  spacing:{name:"Spacing",category:"Pass",tags:["quick","spacing"],description:"Several short hooks settle between underneath zone defenders for a quick rhythm throw."},
  slants:{name:"Slants",category:"Pass",tags:["quick","inside"],description:"Receivers break inside quickly to attack leverage, vacated pressure windows, and RPO-style access."},
  curlFlat:{name:"Curl-Flat",category:"Pass",tags:["quick","flatConflict"],description:"A curl sits behind a flat route to isolate the curl-flat defender."},
  cornerFlat:{name:"Corner-Flat",category:"Pass",tags:["flood","flatConflict"],description:"A corner route and flat route create a two-level sideline stretch."},
  posts:{name:"Double Posts",category:"Pass",tags:["post","vertical","shot"],description:"Two post routes attack split-safety leverage and the middle of the field."},
  doubleMove:{name:"Double Moves",category:"Pass",tags:["vertical","shot"],description:"Outside receivers sell a short break before accelerating vertically."},
  rbScreen:{name:"Running Back Screen",category:"Pass",tags:["screen","back"],description:"The back delays, releases behind the rush, and follows interior blockers into space."},
  wrScreen:{name:"Wide Receiver Screen",category:"Pass",tags:["screen","perimeter"],description:"A perimeter receiver catches behind immediate lead blocks from nearby receivers."},
  teScreen:{name:"Tight End Screen",category:"Pass",tags:["screen","inside"],description:"The tight end delays through the line and releases behind interior screen blockers."},
  playActionShot:{name:"Play-Action Shot",category:"Pass",tags:["shot","playAction","cross"],description:"A run fake holds the second level while a post and deep crossing route attack behind it."},
  insideZone:{name:"Inside Zone",category:"Run",tags:["runInside","zoneRun"],description:"The back presses an interior landmark and reads the first down lineman outside the center."},
  outsideZone:{name:"Outside Zone",category:"Run",tags:["runOutside","zoneRun"],description:"The back stretches toward the edge before choosing the bounce, bang, or bend track."},
  splitZone:{name:"Split Zone",category:"Run",tags:["runInside","zoneRun","kickout"],description:"Inside zone action pairs with a slicing tight end or H-back across the formation."},
  duo:{name:"Duo",category:"Run",tags:["runInside","downhill"],description:"Vertical double teams create a downhill track with the back reading the middle linebacker."},
  power:{name:"Power",category:"Run",tags:["gapRun","puller","runInside"],description:"A backside guard pulls to lead through the strong-side interior gap."},
  counter:{name:"Counter",category:"Run",tags:["gapRun","puller","misdirection"],description:"The back takes a counter step while pullers lead toward the opposite-side gap."},
  trap:{name:"Trap",category:"Run",tags:["gapRun","puller","runInside"],description:"A quick puller traps an interior defender while the back hits vertically."},
  stretch:{name:"Stretch",category:"Run",tags:["runOutside","zoneRun"],description:"The back widens aggressively to force the defense to run laterally before cutting upfield."},
  toss:{name:"Toss",category:"Run",tags:["runOutside","perimeter"],description:"The quarterback pitches the ball immediately and the back races to the perimeter behind lead blocks."},
  draw:{name:"Draw",category:"Run",tags:["runInside","delay"],description:"Pass-set action invites the rush before the back takes a delayed interior handoff."},
  readOption:{name:"Read Option",category:"Run",tags:["option","runOutside","read"],description:"The quarterback reads an edge defender and either gives the zone track or keeps outside."},
  speedOption:{name:"Speed Option",category:"Run",tags:["option","perimeter","read"],description:"The quarterback attacks the edge with a pitch relationship outside."},
  qbPower:{name:"Quarterback Power",category:"Run",tags:["gapRun","qbRun","puller"],description:"The quarterback follows a lead blocker and puller through the designed power gap."},
  jetSweep:{name:"Jet Sweep",category:"Run",tags:["runOutside","motion","perimeter"],description:"A slot receiver takes the ball at speed across the formation and attacks the edge."},
  izBubble:{name:"Inside Zone + Bubble",category:"RPO",tags:["rpo","runInside","bubble"],description:"Inside zone is paired with a perimeter bubble based on box count and overhang leverage."},
  izGlance:{name:"Inside Zone + Glance",category:"RPO",tags:["rpo","runInside","glance"],description:"Inside zone conflicts a second-level defender while the receiver runs a glance route behind him."},
  izStick:{name:"Inside Zone + Stick",category:"RPO",tags:["rpo","runInside","stick"],description:"Inside zone is paired with a stick/flat access concept to the perimeter."},
  readBubble:{name:"Read Option + Bubble",category:"RPO",tags:["rpo","option","bubble","read"],description:"The quarterback combines an edge read with a bubble throw based on the overhang defender."},
  powerRead:{name:"Power Read",category:"RPO",tags:["option","gapRun","read","perimeter"],description:"The quarterback reads the edge while the sweep path and quarterback power track attack opposite spaces."}
};
const OFFENSIVE_CONCEPT_CATEGORIES=["Pass","Run","RPO"];
'''.strip()
replace_once(
    "let scoutPreviewPackage=null;",
    concept_data + "\nlet scoutPreviewPackage=null;",
    "offensive concept data",
)
replace_once(
    'function emptyScoutReport(){return{opponent:"",week:"",tempo:"Balanced",tendency:"Balanced",personnel:["11"],mobileQB:false,rpo:false,concepts:"",notes:"",set:"gun2x2",strength:"right",situation:"Base Defense",macroSlot:null,matchups:[]}}',
    'function emptyScoutReport(){return{opponent:"",week:"",tempo:"Balanced",tendency:"Balanced",personnel:["11"],mobileQB:false,rpo:false,concepts:"",notes:"",set:"gun2x2",concept:"fourVerticals",strength:"right",situation:"Base Defense",macroSlot:null,matchups:[]}}',
    "default offensive concept",
)

normalize_scout = r'''function normalizeScoutReport(raw){
  const base=emptyScoutReport(),validSets=new Set(Object.keys(OFFENSIVE_SCOUT_SETS)),validConcepts=new Set(Object.keys(OFFENSIVE_SCOUT_CONCEPTS)),validIds=new Set(Object.keys(TEAM_PLAYBOOKS));
  const matchups=Array.isArray(raw?.matchups)?raw.matchups.filter(item=>item&&item.package&&PLAY_DB[item.package.formation]?.includes(item.package.play)).map(item=>({...item,concept:validConcepts.has(item.concept)?item.concept:"fourVerticals"})).slice(-20):[];
  return {...base,...raw,opponent:validIds.has(raw?.opponent)?raw.opponent:"",personnel:Array.isArray(raw?.personnel)?raw.personnel.filter(v=>["10","11","12","20","21"].includes(v)):[],set:validSets.has(raw?.set)?raw.set:"gun2x2",concept:validConcepts.has(raw?.concept)?raw.concept:"fourVerticals",strength:raw?.strength==="left"?"left":"right",macroSlot:Number.isInteger(raw?.macroSlot)?raw.macroSlot:null,matchups};
}'''
sub_once(r"function normalizeScoutReport\(raw\)\{.*?\n\}", normalize_scout, "normalize scout report")

concept_helpers = r'''
function populateScoutConcepts(report=getScoutReport()){
  const select=el("scoutConcept"),current=report.concept;select.innerHTML="";
  OFFENSIVE_CONCEPT_CATEGORIES.forEach(category=>{
    const group=document.createElement("optgroup");group.label=category;
    Object.entries(OFFENSIVE_SCOUT_CONCEPTS).filter(([,concept])=>concept.category===category).forEach(([id,concept])=>{const option=document.createElement("option");option.value=id;option.textContent=concept.name;group.appendChild(option)});
    select.appendChild(group);
  });
  select.value=OFFENSIVE_SCOUT_CONCEPTS[current]?current:"fourVerticals";
}
function scoutSetTargets(set,strength){
  const players=set.players.map(([name,x,y],index)=>({name,x,y,index})),skill=players.filter(player=>!/^(LT|LG|C|RG|RT|QB)$/.test(player.name)),receivers=skill.filter(player=>!/^(RB|FB)$/.test(player.name)).sort((a,b)=>a.x-b.x),backs=skill.filter(player=>/^(RB|FB)$/.test(player.name)),qb=players.find(player=>player.name==="QB");
  const strongRight=strength==="right",strong=receivers.filter(player=>strongRight?player.x>=500:player.x<=500),weak=receivers.filter(player=>strongRight?player.x<500:player.x>500);
  const outside=list=>[...list].sort((a,b)=>strongRight?b.x-a.x:a.x-b.x)[0]||receivers[receivers.length-1]||skill[0];
  const inside=list=>[...list].sort((a,b)=>Math.abs(a.x-500)-Math.abs(b.x-500))[0]||receivers[Math.floor(receivers.length/2)]||skill[0];
  const weakOutside=[...weak].sort((a,b)=>strongRight?a.x-b.x:b.x-a.x)[0]||receivers[0]||skill[0],weakInside=[...weak].sort((a,b)=>Math.abs(a.x-500)-Math.abs(b.x-500))[0]||weakOutside;
  return{players,skill,receivers,backs,qb,strongRight,dir:strongRight?1:-1,strongOutside:outside(strong),strongInside:inside(strong),weakOutside,weakInside,back:backs.find(player=>player.name==="RB")||backs[0]||inside(strong),fullback:backs.find(player=>player.name==="FB")||backs[1]||backs[0]};
}
function scoutPath(svg,start,points,kind="pass",dash=false){
  if(!start||!points.length)return;
  const style={pass:["#ff96d7","scoutPassArrow",4],run:["#f4f8ff","scoutRunArrow",5],read:["#ffd66f","scoutReadArrow",4],block:["#9fb4c9","scoutBlockArrow",4]}[kind]||["#ff96d7","scoutPassArrow",4];
  const all=[[start.x,start.y],...points],path=svgEl("path",{d:all.map(([x,y],index)=>`${index?"L":"M"}${x} ${y}`).join(" "),fill:"none",stroke:style[0],"stroke-width":style[2],"stroke-linecap":"round","stroke-linejoin":"round","marker-end":`url(#${style[1]})`});
  if(dash)path.setAttribute("stroke-dasharray","9 6");svg.appendChild(path);
}
function drawOffensiveConcept(svg,set,conceptId,strength){
  const concept=OFFENSIVE_SCOUT_CONCEPTS[conceptId]||OFFENSIVE_SCOUT_CONCEPTS.fourVerticals,t=scoutSetTargets(set,strength),d=t.dir,so=t.strongOutside,si=t.strongInside,wo=t.weakOutside,wi=t.weakInside,back=t.back,qb=t.qb,fb=t.fullback;
  const pass=(start,points)=>scoutPath(svg,start,points,"pass"),run=(start,points)=>scoutPath(svg,start,points,"run"),read=(start,points)=>scoutPath(svg,start,points,"read",true),block=(start,points)=>scoutPath(svg,start,points,"block",true),vertical=(player,xShift=0)=>pass(player,[[player.x+xShift,360],[player.x+xShift,110]]),flat=(player)=>pass(player,[[player.x+d*70,500],[player.x+d*180,470]]),insideRun=()=>run(back,[[back.x-d*25,570],[500+d*35,485],[500+d*20,300]]),bubble=()=>pass(so,[[so.x-d*25,555],[so.x-d*95,525],[so.x-d*165,495]]);
  switch(conceptId){
    case"fourVerticals":{const targets=[...t.receivers].sort((a,b)=>a.x-b.x);targets.slice(0,4).forEach((player,index)=>vertical(player,index===1?25:index===2?-25:0));break}
    case"mesh":pass(si,[[si.x,430],[wi.x,400],[wo.x,390]]);pass(wi,[[wi.x,425],[si.x,395],[so.x,385]]);vertical(so);pass(wo,[[wo.x,350],[500,210]]);break;
    case"shallowCross":pass(wi,[[wi.x,430],[500,410],[so.x,395]]);pass(si,[[si.x,330],[500,300],[wo.x,300]]);vertical(so);vertical(wo);break;
    case"drive":pass(si,[[si.x,430],[500,410],[wo.x,400]]);pass(wi,[[wi.x,330],[500,300],[so.x,300]]);vertical(so);break;
    case"levels":{const group=[so,si,wi].filter(Boolean);group.forEach((player,index)=>pass(player,[[player.x,420-index*70],[500-d*(40+index*45),420-index*70]]));break}
    case"dagger":vertical(si,d*20);pass(so,[[so.x,315],[500+d*40,280],[500-d*180,280]]);vertical(wo);break;
    case"mills":pass(so,[[so.x,330],[500+d*80,120],[500,90]]);pass(si,[[si.x,310],[500,285],[500-d*170,285]]);break;
    case"flood":vertical(so);pass(si,[[si.x,350],[si.x+d*110,255],[si.x+d*185,220]]);flat(back);break;
    case"sail":vertical(so);pass(si,[[si.x,350],[si.x+d*135,245],[si.x+d*215,225]]);flat(wi||back);break;
    case"smash":pass(so,[[so.x,420],[so.x-d*20,440]]);pass(si,[[si.x,350],[si.x+d*120,210]]);break;
    case"stick":pass(si,[[si.x,420],[si.x+d*45,395]]);flat(back);vertical(so);break;
    case"spacing":{const targets=[wo,wi,si,so].filter(Boolean).slice(0,3);targets.forEach((player,index)=>pass(player,[[player.x,405-index*8],[player.x+(index-1)*55,390-index*8]]));break}
    case"slants":t.receivers.slice(0,4).forEach(player=>pass(player,[[player.x,435],[player.x+(player.x<500?120:-120),330]]));break;
    case"curlFlat":pass(so,[[so.x,350],[so.x-d*25,385]]);flat(si||back);break;
    case"cornerFlat":pass(si,[[si.x,350],[si.x+d*135,205]]);flat(back);break;
    case"posts":pass(so,[[so.x,330],[500+d*70,120]]);pass(wo,[[wo.x,330],[500-d*70,120]]);break;
    case"doubleMove":[so,wo].filter(Boolean).forEach(player=>pass(player,[[player.x,410],[player.x-d*(player===wo?1:-1)*25,435],[player.x,360],[player.x,110]]));break;
    case"rbScreen":pass(back,[[back.x-d*20,585],[back.x+d*70,560],[back.x+d*190,470],[back.x+d*235,360]]);t.players.filter(player=>/^(LG|C|RG)$/.test(player.name)).forEach((player,index)=>block(player,[[player.x+d*(70+index*35),525],[player.x+d*(155+index*35),450]]));break;
    case"wrScreen":pass(so,[[so.x-d*25,555],[so.x-d*95,525],[so.x-d*145,490]]);[si,t.receivers.find(player=>player!==so&&player!==si&&Math.sign(player.x-500)===Math.sign(so.x-500))].filter(Boolean).forEach((player,index)=>block(player,[[so.x-d*(80+index*45),470],[so.x-d*(105+index*50),400]]));break;
    case"teScreen":pass(si,[[si.x,520],[si.x-d*35,500],[500+d*40,445],[500+d*90,350]]);t.players.filter(player=>/^(LG|C|RG)$/.test(player.name)).forEach((player,index)=>block(player,[[500+d*(35+index*45),500],[500+d*(55+index*55),420]]));break;
    case"playActionShot":run(back,[[500+d*25,525],[500+d*45,480]]);pass(so,[[so.x,330],[500+d*65,105]]);pass(wi,[[wi.x,360],[500,280],[so.x-d*80,235]]);break;
    case"insideZone":insideRun();break;
    case"outsideZone":run(back,[[back.x+d*70,560],[500+d*180,510],[500+d*320,420],[500+d*400,300]]);break;
    case"splitZone":insideRun();block(wi||fb,[[500-d*80,545],[500+d*95,505],[500+d*155,455]]);break;
    case"duo":run(back,[[500,520],[500+d*15,420],[500+d*10,260]]);break;
    case"power":run(back,[[back.x-d*20,565],[500+d*65,500],[500+d*95,330]]);{const guard=t.players.find(player=>player.name===(d>0?"LG":"RG"));block(guard,[[500-d*35,550],[500+d*65,505],[500+d*110,420]])}break;
    case"counter":run(back,[[back.x+d*45,585],[back.x-d*40,555],[500-d*90,485],[500-d*140,330]]);t.players.filter(player=>player.name===(d>0?"RG":"LG")||player.name===(d>0?"RT":"LT")).forEach((player,index)=>block(player,[[500+d*(35+index*40),555],[500-d*(80+index*50),500],[500-d*(125+index*45),420]]));break;
    case"trap":run(back,[[500,535],[500+d*30,450],[500+d*25,300]]);{const guard=t.players.find(player=>player.name===(d>0?"LG":"RG"));block(guard,[[500-d*55,555],[500+d*40,505]])}break;
    case"stretch":run(back,[[back.x+d*90,565],[500+d*245,525],[500+d*375,455],[500+d*430,330]]);break;
    case"toss":read(qb,[[qb.x+d*80,590],[qb.x+d*145,565]]);run(back,[[back.x+d*105,575],[500+d*250,520],[500+d*390,430],[500+d*440,320]]);break;
    case"draw":read(qb,[[qb.x,610],[qb.x,595]]);run(back,[[back.x,585],[500,530],[500+d*25,410],[500+d*15,270]]);break;
    case"readOption":run(back,[[back.x+d*75,565],[500+d*170,500],[500+d*260,390]]);read(qb,[[qb.x-d*40,565],[500-d*135,480],[500-d*210,360]]);break;
    case"speedOption":read(qb,[[qb.x+d*80,565],[500+d*180,485],[500+d*275,365]]);run(back,[[back.x+d*140,580],[500+d*280,500],[500+d*390,390]]);break;
    case"qbPower":read(qb,[[qb.x-d*20,565],[500+d*65,495],[500+d*95,330]]);block(fb||back,[[500+d*35,530],[500+d*95,430]]);break;
    case"jetSweep":{const jet=d>0?wi:si;run(jet,[[500-d*90,555],[500+d*90,535],[500+d*260,470],[500+d*390,360]]);break}
    case"izBubble":insideRun();bubble();break;
    case"izGlance":insideRun();pass(so,[[so.x,430],[so.x-d*115,320]]);break;
    case"izStick":insideRun();pass(si,[[si.x,420],[si.x+d*45,395]]);flat(so);break;
    case"readBubble":run(back,[[back.x+d*70,565],[500+d*170,500],[500+d*250,400]]);read(qb,[[qb.x-d*40,565],[500-d*140,450]]);bubble();break;
    case"powerRead":run(si||back,[[500-d*90,555],[500+d*105,525],[500+d*260,430]]);read(qb,[[qb.x-d*20,565],[500-d*70,500],[500-d*95,340]]);block(fb||back,[[500-d*30,535],[500-d*90,430]]);break;
  }
}
'''.strip()
replace_once(
    "function scoutDefenseCoords(ids){",
    concept_helpers + "\nfunction scoutDefenseCoords(ids){",
    "concept drawing helpers",
)

new_draw_field = r'''function drawScoutField(){
  const svg=el("scoutField"),report=getScoutReport(),set=OFFENSIVE_SCOUT_SETS[report.set],concept=OFFENSIVE_SCOUT_CONCEPTS[report.concept],pkg=activeScoutPackage(report);svg.innerHTML="";
  const defs=svgEl("defs");
  [["scoutArrow","#f4f8ff"],["scoutPassArrow","#ff96d7"],["scoutRunArrow","#f4f8ff"],["scoutReadArrow","#ffd66f"],["scoutBlockArrow","#9fb4c9"]].forEach(([id,fill])=>{const marker=svgEl("marker",{id,viewBox:"0 0 10 10",refX:"8",refY:"5",markerWidth:"6",markerHeight:"6",orient:"auto"});marker.appendChild(svgEl("path",{d:"M0 0 L10 5 L0 10 Z",fill}));defs.appendChild(marker)});svg.appendChild(defs);
  svg.appendChild(svgEl("rect",{x:0,y:0,width:1000,height:620,fill:"#123e2a"}));for(let i=0;i<10;i++){svg.appendChild(svgEl("rect",{x:i*100,y:0,width:100,height:620,fill:i%2?"#184a32":"#123e2a"}));svg.appendChild(svgEl("line",{x1:i*100,y1:0,x2:i*100,y2:620,stroke:"rgba(255,255,255,.13)","stroke-width":2}))}svg.appendChild(svgEl("line",{x1:0,y1:525,x2:1000,y2:525,stroke:"#fff","stroke-width":4}));
  drawOffensiveConcept(svg,set,report.concept,report.strength);
  set.players.forEach(([name,x,y])=>{svg.appendChild(svgEl("circle",{cx:x,cy:y,r:name==="QB"?16:12,fill:"rgba(230,235,241,.88)",stroke:"#fff","stroke-width":2}));const t=svgEl("text",{x,y:y+3,"text-anchor":"middle",fill:"#071018","font-size":name==="QB"?9:7,"font-weight":900});t.textContent=name;svg.appendChild(t)});
  const conceptLabel=svgEl("text",{x:18,y:28,fill:"#fff","font-size":13,"font-weight":850});conceptLabel.textContent=`${concept.category.toUpperCase()}: ${concept.name}`;svg.appendChild(conceptLabel);
  if(!pkg){const t=svgEl("text",{x:500,y:260,"text-anchor":"middle",fill:"#d8e8f5","font-size":20,"font-weight":800});t.textContent="Save a macro, then select it here";svg.appendChild(t);return}
  const assignments=pkg.assignments||{},ids=Object.keys(assignments),coords=scoutDefenseCoords(ids),colors={deep:["rgba(101,217,239,.22)","#65d9ef"],under:["rgba(126,227,154,.22)","#7ee39a"],flat:["rgba(255,214,111,.23)","#ffd66f"],spy:["rgba(193,155,255,.24)","#c19bff"],pressure:["rgba(255,173,100,.12)","#ffad64"],hidden:["rgba(127,145,164,.06)","#7f91a4"]};
  ids.forEach(id=>{const [x,y]=coords[id],key=assignments[id],[tx,ty,rx,ry,type]=scoutGeometry(key,x,report.strength),[,stroke]=colors[type];if(type==="deep"||type==="under"||type==="flat"||type==="spy"){svg.appendChild(svgEl("ellipse",{cx:tx,cy:ty,rx,ry,fill:colors[type][0],stroke,"stroke-width":2}));svg.appendChild(svgEl("line",{x1:x,y1:y,x2:tx,y2:ty,stroke,"stroke-width":2,"stroke-dasharray":"7 5","marker-end":"url(#scoutArrow)"}))}else if(type==="pressure"){svg.appendChild(svgEl("line",{x1:x,y1:y,x2:tx,y2:ty,stroke,"stroke-width":3,"marker-end":"url(#scoutArrow)"}))}svg.appendChild(svgEl("circle",{cx:x,cy:y,r:16,fill:"#0d2434",stroke,"stroke-width":3}));const label=svgEl("text",{x,y:y+3,"text-anchor":"middle",fill:"#fff","font-size":8,"font-weight":900});label.textContent=id;svg.appendChild(label);if(type==="hidden"){const m=svgEl("text",{x,y:y-22,"text-anchor":"middle",fill:"#dce6ef","font-size":8,"font-weight":900});m.textContent="MAN";svg.appendChild(m)}});
}'''
sub_once(r"function drawScoutField\(\)\{.*?\n\}\nfunction scoutAlerts", new_draw_field + "\nfunction scoutAlerts", "enhanced scout field")

new_alerts = r'''function scoutAlerts(report=getScoutReport(),pkg=activeScoutPackage(report)){
  if(!pkg)return[{level:"medium",title:"No saved macro selected",detail:"Build and save a macro in the existing macro builder, then select that slot for the matchup lab."}];
  const set=OFFENSIVE_SCOUT_SETS[report.set],concept=OFFENSIVE_SCOUT_CONCEPTS[report.concept],tags=concept.tags||[],a=pkg.assignments||{},entries=Object.entries(a),values=entries.map(([,v])=>v),count=re=>values.filter(v=>re.test(v)).length,alerts=[],shell=inferShell(pkg.play||"");
  const blitz=count(/blitz/),contain=count(/qbContain/),spy=count(/qbSpy/),seam=count(/seamFlat|quarterFlat|vertHook|middleRead|threeRecHook/),hook=count(/Hook|hookCurl|srcHook/),flat=count(/Flat|curlFlat|hardFlat|cloudFlat|softSquat|flatTrap/),deep=count(/deepHalf|deepThird|outsideThird|insideThird|deepQuarter/),man=count(/manHidden/),box=entries.filter(([id,v])=>/SAM|MIKE|WILL|JACK|LB|RLE|RRE|RDT|NT|DT|LE|RE/.test(id)&&!/deep|outsideThird|insideThird|Flat/.test(v)).length;
  if(report.mobileQB&&!contain&&!spy)alerts.push({level:"high",title:"No dedicated contain or spy",detail:"The scout marks a mobile quarterback, but this macro snapshot has no QB contain or spy responsibility."});
  if(report.mobileQB&&(contain||spy))alerts.push({level:"good",title:"Quarterback control present",detail:`This macro includes ${contain} contain and ${spy} spy responsibility${contain+spy===1?"":"ies"}.`});
  if(set.tags.includes("empty")&&man>=4)alerts.push({level:"medium",title:"Empty formation man-match stress",detail:"Verify cross-field matches, slot leverage, and traffic rules before relying on this call against empty."});
  if(set.tags.includes("bunch")&&flat<2)alerts.push({level:"high",title:"Bunch leverage stress",detail:"The macro shows limited flat/curl-flat structure. Confirm banjo, point, and outside-release responsibilities."});
  if(tags.includes("vertical")){if(deep<3)alerts.push({level:"high",title:"Vertical concept threatens limited deep structure",detail:`${concept.name} attacks vertically while the macro shows only ${deep} deep responsibility${deep===1?"":"ies"}.`});if(shell==="cover2"&&seam<2)alerts.push({level:"high",title:"Split-safety seam stress",detail:"Four-vertical/post structure can divide the deep halves without two reliable seam or middle-carry defenders."});if(shell==="cover3"&&seam<2)alerts.push({level:"medium",title:"Three-deep seam stress",detail:"The inside vertical routes can hold the middle third and isolate the outside thirds."})}
  if(tags.includes("cross")){if(man>=4)alerts.push({level:"medium",title:"Crossing-route traffic in man coverage",detail:"Confirm pass-offs, trailing leverage, and cross-field match rules against the selected crossing concept."});if(hook+seam<3)alerts.push({level:"medium",title:"Limited inside traffic control",detail:"The concept layers crossers through the middle while the macro shows limited hook, seam, or middle-carry presence."})}
  if(tags.includes("flood")){if(flat<1||deep<2)alerts.push({level:"high",title:"Sideline flood conflict",detail:"The concept creates a flat/intermediate/deep stretch without a complete three-level defensive structure."});else alerts.push({level:"medium",title:"Three-level sideline stretch",detail:"Identify which defender takes the flat, sail/corner, and vertical routes as they enter one sideline."})}
  if(tags.includes("smash")||tags.includes("highLow")){alerts.push({level:"medium",title:"Flat/deep-half high-low",detail:"Smash places the flat defender underneath a corner route and can stress split-safety leverage."})}
  if(tags.includes("quick")&&blitz>=5)alerts.push({level:"high",title:"Quick-game answer behind pressure",detail:`The macro sends ${blitz} rushers while ${concept.name} is designed to deliver the ball quickly into vacated space.`});
  if(tags.includes("screen")){if(blitz>=5)alerts.push({level:"high",title:"Screen exposure behind heavy pressure",detail:`The macro sends ${blitz} rushers into a concept designed to release behind them.`});else alerts.push({level:"medium",title:"Screen retrace responsibility",detail:"Identify the defender responsible for recognizing the release, retracing, and defeating lead blocks."})}
  if(tags.includes("shot")){if(blitz>=5)alerts.push({level:"medium",title:"Protection race on shot concept",detail:"Pressure may reach the quarterback, but a failed rush lane or blocked pressure can expose a large vertical play."});if(deep<3)alerts.push({level:"high",title:"Shot concept versus thin deep coverage",detail:"The selected concept attacks deep with fewer than three deep-zone responsibilities in the macro."})}
  if(tags.includes("runInside")||tags.includes("gapRun")){if(box<6)alerts.push({level:"high",title:"Light box against interior run",detail:`Only ${box} front/box defenders remain structurally available against ${concept.name}.`});else alerts.push({level:"good",title:"Interior box count present",detail:`The macro keeps ${box} front/box defenders structurally available.`})}
  if(tags.includes("runOutside")||tags.includes("perimeter")){if(!contain)alerts.push({level:"medium",title:"Perimeter force must be identified",detail:"The macro has no explicit contain responsibility against a concept designed to reach the edge."});if(flat<1)alerts.push({level:"medium",title:"Limited alley support",detail:"The perimeter concept can stress force and alley support without a visible flat responsibility."})}
  if(tags.includes("puller")||tags.includes("kickout"))alerts.push({level:"medium",title:"Puller and kick-out fit",detail:"Set the spill/box rule and identify who fits inside and outside the puller before using this call."});
  if(tags.includes("option")||tags.includes("read")){if(!contain&&!spy)alerts.push({level:"high",title:"No defined quarterback/edge control",detail:"The option concept can leave the quarterback unaccounted for without contain, a spy, or a declared scrape-exchange rule."});else alerts.push({level:"good",title:"Option control tool present",detail:"The macro includes contain or spy structure that can support the option fit."})}
  if(tags.includes("rpo")){if(blitz>=5)alerts.push({level:"medium",title:"RPO replacement window",detail:"Pressure can widen or remove the conflict defender and create an immediate throw behind him."});if(flat+hook<3)alerts.push({level:"medium",title:"Limited throw-window support",detail:"The attached RPO route attacks an area with limited flat and hook support in the macro."})}
  if(blitz>=5&&!tags.includes("screen")&&!tags.includes("quick"))alerts.push({level:"medium",title:"Hot-outlet and screen exposure",detail:`The saved macro sends ${blitz} rushers. Verify the immediate outlet and screen retrace answer.`});
  if(!alerts.some(item=>item.level==="high"))alerts.push({level:"good",title:"No major structural red flag detected",detail:"The concept still requires in-game verification for motion, releases, blocking rules, personnel ratings, and user control."});
  return alerts;
}'''
sub_once(r"function scoutAlerts\(report=getScoutReport\(\),pkg=activeScoutPackage\(report\)\)\{.*?\n\}\nfunction populateScoutMacros", new_alerts + "\nfunction populateScoutMacros", "concept-aware scout alerts")

new_saved = r'''function renderScoutSaved(report=getScoutReport()){
  const list=el("scoutSavedList");list.innerHTML="";el("scoutSavedCount").textContent=`${report.matchups.length} saved`;if(!report.matchups.length){const empty=document.createElement("div");empty.className="empty-state";empty.textContent="No tested macro matchups saved yet.";list.appendChild(empty);return}report.matchups.slice().reverse().forEach(item=>{const concept=OFFENSIVE_SCOUT_CONCEPTS[item.concept]||OFFENSIVE_SCOUT_CONCEPTS.fourVerticals,row=document.createElement("article");row.className="scout-saved-row";const main=document.createElement("div"),title=document.createElement("strong"),meta=document.createElement("span");title.textContent=`${OFFENSIVE_SCOUT_SETS[item.set]?.name||item.set} • ${concept.name} — ${item.package.name||item.package.play}`;meta.textContent=`${concept.category} • ${item.situation} • ${item.package.formation} — ${item.package.play} • ${item.alertCount} alert${item.alertCount===1?"":"s"}`;main.append(title,meta);const actions=document.createElement("div");actions.className="scout-saved-actions";const preview=document.createElement("button");preview.textContent="Preview";preview.onclick=()=>{scoutPreviewPackage={...clonePackage(item.package),macroSlot:item.macroSlot};const r=getScoutReport();r.set=item.set;r.concept=item.concept;r.strength=item.strength;r.situation=item.situation;storeScoutReport(r);renderScoutReport()};const gameplan=document.createElement("button");gameplan.textContent="Gameplan";gameplan.onclick=()=>sendScoutPackageToGameplan(item.package,item.macroSlot,`Saved Scout: ${OFFENSIVE_SCOUT_SETS[item.set]?.name||item.set} • ${concept.name}`,item.situation,item.concept,item.set);const remove=document.createElement("button");remove.className="remove";remove.textContent="Remove";remove.onclick=()=>{const r=getScoutReport();r.matchups=r.matchups.filter(saved=>saved.id!==item.id);storeScoutReport(r);renderScoutReport()};actions.append(preview,gameplan,remove);row.append(main,actions);list.appendChild(row)})
}'''
sub_once(r"function renderScoutSaved\(report=getScoutReport\(\)\)\{.*?\n\}", new_saved, "saved concept matchups")

new_render = r'''function renderScoutReport(){
  const report=getScoutReport(),set=OFFENSIVE_SCOUT_SETS[report.set],concept=OFFENSIVE_SCOUT_CONCEPTS[report.concept];populateScoutMacros(report);populateScoutConcepts(report);const bind=(id,value)=>{const node=el(id);if(document.activeElement!==node)node.value=value};bind("scoutOpponent",report.opponent);bind("scoutWeek",report.week);bind("scoutTempo",report.tempo);bind("scoutTendency",report.tendency);bind("scoutConcepts",report.concepts);bind("scoutNotes",report.notes);bind("scoutOffensiveSet",report.set);bind("scoutConcept",report.concept);bind("scoutStrength",report.strength);bind("scoutSituation",report.situation);el("scoutConceptDescription").innerHTML=`<strong>${concept.category}: ${concept.name}</strong><br>${concept.description}`;el("scoutMobileQB").checked=report.mobileQB;el("scoutRPO").checked=report.rpo;document.querySelectorAll('#scoutPersonnelGrid input[type="checkbox"]').forEach(box=>box.checked=report.personnel.includes(box.value));drawScoutField();const pkg=activeScoutPackage(report),alerts=scoutAlerts(report,pkg),summary=el("scoutMatchupSummary");summary.innerHTML="";[set.name,`Personnel ${set.personnel}`,`${concept.category}: ${concept.name}`,pkg?`${pkg.formation} — ${pkg.play}`:"No macro",`Strength ${report.strength.toUpperCase()}`].forEach(value=>{const span=document.createElement("span");span.textContent=value;summary.appendChild(span)});const alertWrap=el("scoutAlerts");alertWrap.innerHTML="";alerts.forEach(item=>{const card=document.createElement("div");card.className=`scout-alert ${item.level}`;const strong=document.createElement("strong"),detail=document.createElement("span");strong.textContent=item.title;detail.textContent=item.detail;card.append(strong,detail);alertWrap.appendChild(card)});const disabled=!pkg;["saveScoutMatchup","sendScoutToGameplan","loadScoutInBuilder"].forEach(id=>el(id).disabled=disabled);renderScoutSaved(report)
}'''
sub_once(r"function renderScoutReport\(\)\{.*?\n\}", new_render, "render concept scout report")

new_update = 'function updateScoutReportFromInputs(){const report=getScoutReport();report.opponent=el("scoutOpponent").value;report.week=el("scoutWeek").value;report.tempo=el("scoutTempo").value;report.tendency=el("scoutTendency").value;report.personnel=[...document.querySelectorAll(\'#scoutPersonnelGrid input[type="checkbox"]:checked\')].map(box=>box.value);report.mobileQB=el("scoutMobileQB").checked;report.rpo=el("scoutRPO").checked;report.concepts=el("scoutConcepts").value;report.notes=el("scoutNotes").value;report.set=el("scoutOffensiveSet").value;report.concept=el("scoutConcept").value;report.strength=el("scoutStrength").value;report.situation=el("scoutSituation").value;report.macroSlot=el("scoutMacro").value===""?null:Number(el("scoutMacro").value);scoutPreviewPackage=null;storeScoutReport(report);renderScoutReport()}'
sub_once(r"function updateScoutReportFromInputs\(\)\{.*?\}", new_update, "update concept scout inputs")

new_save = 'function saveScoutMatchup(){const report=getScoutReport(),pkg=activeScoutPackage(report);if(!pkg)return;const alerts=scoutAlerts(report,pkg);report.matchups.push({id:`scout-${Date.now()}-${Math.random().toString(36).slice(2,8)}`,set:report.set,concept:report.concept,strength:report.strength,situation:report.situation,macroSlot:scoutPackageSlot(report),package:clonePackage(pkg),alertCount:alerts.filter(item=>item.level!=="good").length,savedAt:new Date().toISOString()});report.matchups=report.matchups.slice(-20);storeScoutReport(report);renderScoutReport()}'
sub_once(r"function saveScoutMatchup\(\)\{.*?\}", new_save, "save concept matchup")

new_gameplan = 'function sendScoutPackageToGameplan(pkg=activeScoutPackage(),macroSlot=scoutPackageSlot(),source="Opponent Scout Lab",situation=getScoutReport().situation,conceptId=getScoutReport().concept,setId=getScoutReport().set){if(!pkg)return;const report=getScoutReport(),plan=getGameplan(),set=OFFENSIVE_SCOUT_SETS[setId]||OFFENSIVE_SCOUT_SETS[report.set],concept=OFFENSIVE_SCOUT_CONCEPTS[conceptId]||OFFENSIVE_SCOUT_CONCEPTS[report.concept];if(report.opponent)plan.opponent=report.opponent;if(report.week)plan.week=report.week;plan.entries.push({id:`call-${Date.now()}-${Math.random().toString(36).slice(2,8)}`,situation,note:[`vs ${set.name} • ${concept.name}`,report.concepts.trim()].filter(Boolean).join(" • "),source,macroSlot:Number.isInteger(macroSlot)?macroSlot:null,package:clonePackage(pkg)});storeGameplan(plan);renderGameplan();el("gameplanPanel")?.scrollIntoView({behavior:"smooth",block:"start"})}'
sub_once(r"function sendScoutPackageToGameplan\(.*?\}\nfunction clearScoutReport", new_gameplan + "\nfunction clearScoutReport", "gameplan concept metadata")

replace_once(
    '["scoutOpponent","scoutWeek","scoutTempo","scoutTendency","scoutConcepts","scoutNotes","scoutOffensiveSet","scoutStrength","scoutSituation","scoutMacro","scoutMobileQB","scoutRPO"]',
    '["scoutOpponent","scoutWeek","scoutTempo","scoutTendency","scoutConcepts","scoutNotes","scoutOffensiveSet","scoutConcept","scoutStrength","scoutSituation","scoutMacro","scoutMobileQB","scoutRPO"]',
    "concept event binding",
)

replace_once(
    "Record personnel, tempo, concepts, mobile-QB and RPO tendencies, then test a saved macro against a generic offensive set without changing the macro slot.",
    "Record personnel and tendencies, select a base offensive concept, then view its route or run art against a saved defensive macro without changing the macro slot.",
    "help concept wording",
)
replace_once(
    '<article class="release-item"><strong>Opponent scout report and macro matchup lab</strong><span>Track offensive tendencies, place saved macro assignments over generic offensive sets, flag structural stress, save tested matchups, and send them to the weekly gameplan without changing macro slots.</span></article>',
    '<article class="release-item"><strong>Base offensive concept scouting</strong><span>Select core pass, run, option, screen, and RPO concepts; draw their route/run art over the offensive shell; and generate concept-specific structural alerts against saved macros.</span></article>\n            <article class="release-item"><strong>Opponent scout report and macro matchup lab</strong><span>Track offensive tendencies, place saved macro assignments over generic offensive sets, flag structural stress, save tested matchups, and send them to the weekly gameplan without changing macro slots.</span></article>',
    "concept release note",
)

INDEX.write_text(text, encoding="utf-8")
readme = README.read_text(encoding="utf-8")
marker = "- Opponent Scout Report and Macro Matchup Lab with offensive tendency tracking, generic offensive-set shells, read-only saved-macro visualization, structural coaching alerts, saved matchup notes, weekly-gameplan integration, local persistence, and backup support\n"
feature = "- Base Offensive Concept layer with grouped pass, run, option, screen, and RPO selections; route/run visualization; concept-specific defensive stress alerts; and concept metadata preserved in saved scout matchups and Weekly Gameplan calls\n"
if feature not in readme:
    if marker not in readme:
        raise SystemExit("README scout lab marker missing")
    readme = readme.replace(marker, marker + feature, 1)
README.write_text(readme, encoding="utf-8")


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key=="id" and value:self.ids.append(value)

parser=IdCollector();parser.feed(text)
new_ids=["scoutConcept","scoutConceptDescription"]
for item in new_ids:
    if parser.ids.count(item)!=1:raise SystemExit(f"Expected exactly one #{item}, found {parser.ids.count(item)}")
preserved=["libraryView","family","formation","play","field","playerGrid","assignmentGroups","macroList","saveMacro","overwriteMacro","clearMacros","scoutLabPanel","scoutOffensiveSet","scoutMacro","scoutField","gameplanPanel","gameplanCallSheet"]
for item in preserved:
    if parser.ids.count(item)!=1:raise SystemExit(f"Fundamental existing control #{item} changed unexpectedly")
required=["const OFFENSIVE_SCOUT_CONCEPTS=","function drawOffensiveConcept","report.concept=el(\"scoutConcept\").value","concept:report.concept","vs ${set.name} • ${concept.name}"]
for item in required:
    if text.count(item)!=1:raise SystemExit(f"Expected one offensive concept integration marker: {item}")
concept_count=len(re.findall(r'^  [A-Za-z][A-Za-z0-9]+:\{name:',text,re.M))
if concept_count<35:raise SystemExit(f"Expected at least 35 base concepts, found {concept_count}")
script=re.search(r"<script>(.*)</script>",text,re.S)
if not script:raise SystemExit("Could not extract application JavaScript")
Path("/tmp/cfb27-offensive-concepts.js").write_text(script.group(1),encoding="utf-8")
print(f"Offensive concept scout patch validation passed with {concept_count} concepts.")
