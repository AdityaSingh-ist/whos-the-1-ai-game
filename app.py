import streamlit as st, streamlit.components.v1 as components
from core.theme import boot, nav, APP, TAG
from core.engine import CH, data
boot(); nav(); B, X = data()
COL = ["#c6ff2e", "#ff3d8b", "#3d5aff", "#ff8a1f", "#fff4e0"]
tile = lambda n, t, d, i: f"<div class='tile' style='--t:{COL[i % 5]};--tc:{'#fff4e0' if COL[i % 5] == '#3d5aff' else '#0d0d12'}'><div class='tn'>{n}</div><div><div class='tt'>{t}</div><div class='td'>{d}</div></div></div>"
sec = lambda t: f"<div class='sec'>{t}</div>"
nums = [(f"{len(B)}", "CASE FILES", "Questions across Units I and II"), ("05", "CHAPTERS", "One mystery, five zones of AI"), (f"0{len(X['bug_hunt'])}", "BUG HUNTS", "Find the one corrupted line"), (f"0{len(X['interrogation'])}", "INTERROGATIONS", "Read the chat, expose the bot")]
feats = [("ELO", "ADAPTIVE", "Your rating picks each next file"), ("BUG", "BUG HUNT", "Spot the wrong step in a BFS, DFS or CSP trace"), ("BOT", "INTERROGATION", "Turing-test style: who is the machine"),
         ("Q&A", "VIVA MODE", "Ten random questions, answer first, then reveal"), ("AID", "LIFELINES", "Narrow Suspects, Lab Tech, Reopen Later"), ("MAP", "WEAK SPOTS", "A radar chart shows what to revise")]
k = 0; parts = ["<div class='hero'><div class='dsp mut'>DSC401 / ARTIFICIAL INTELLIGENCE / UNITS I + II</div><div class='w1'>WHO'S<br>THE 1</div><div class='w2'>THE RA-1 FILES</div><p class='sub'>Ra-1, a rational agent, was corrupted by a rival lab. You are the forensic auditor. Crack five chapters of AI, hunt the bug in its reasoning, expose who did it.</p><div class='dsp grad'>KEEP SCROLLING &gt;&gt;&gt;</div></div>", sec("THE NUMBERS")]
for n, t, d in nums: parts.append(tile(n, t, d, k)); k += 1
parts.append(sec("THE TOOLKIT"))
for n, t, d in feats: parts.append(tile(n, t, d, k)); k += 1
parts.append(sec("THE CHAPTERS"))
for i, (n, ic, d, *_) in enumerate(CH): parts.append(tile(ic, n.upper(), d, k)); k += 1
topics = " / ".join(["TURING TEST", "RATIONAL AGENTS", "PEAS", "STATE SPACE", "PRODUCTION SYSTEMS", "BFS", "DFS", "ITERATIVE DEEPENING", "HILL CLIMBING", "BEST-FIRST", "CSP", "MEANS-END ANALYSIS"])
mq = lambda cls: f"<div class='mq {cls}'><div><span>{topics} / </span><span>{topics} / </span></div></div>"
st.markdown(mq("") + "<div class='rail'>" + "".join(parts) + "</div>" + mq("g"), unsafe_allow_html=True)
JS = """<script>const d=window.parent.document;setInterval(()=>{const r=d.querySelector('.rail');if(r&&!r._w){r._w=1;r.addEventListener('wheel',e=>{if(Math.abs(e.deltaY)>Math.abs(e.deltaX)){r.scrollLeft+=e.deltaY*1.8;e.preventDefault()}},{passive:false})}},400)</script>"""
try: st.iframe(JS, height=1)   # newer Streamlit
except Exception: components.html(JS, height=0)   # older Streamlit
