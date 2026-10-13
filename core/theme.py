import streamlit as st

APP, TAG = "Who's The 1", "The Ra-1 Files"

CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Bungee&family=Bungee+Shade&family=Space+Grotesk:wght@400;600;700&display=swap');
:root{--l:#c6ff2e;--p:#ff3d8b;--b:#3d5aff;--o:#ff8a1f;--c:#fff4e0;--k:#0d0d12}
html,body,.stApp,input,textarea{font-family:'Space Grotesk',sans-serif!important}
h1,h2,h3,.dsp,.stButton>button,.stButton>button p,a[data-testid=stPageLink-NavLink] p{font-family:'Bungee',sans-serif!important;letter-spacing:.02em}
.stApp{background:var(--k);color:var(--c)}
.stApp::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;background:repeating-linear-gradient(115deg,#ffffff0c 0 2px,#0000 2px 28px);animation:slide 5s linear infinite}
@keyframes slide{to{background-position:280px 0}}
@keyframes mq{to{transform:translateX(-50%)}}
@keyframes enter{from{opacity:0;transform:translateX(260px) rotate(16deg) scale(.55)}}
.block-container{position:relative;z-index:1;max-width:1400px;padding:1rem 3vw 3rem 3vw}
header[data-testid=stHeader],footer,[data-testid=stSidebar],[data-testid=collapsedControl]{display:none!important}
h1{font-size:clamp(2.2rem,5vw,4rem)!important;color:var(--l);text-shadow:4px 4px 0 var(--p)}
.grad{color:var(--l);text-shadow:4px 4px 0 var(--p)}
.glass{background:#14141cdd;backdrop-filter:blur(14px);border:3px solid var(--c);border-radius:20px;padding:20px 24px;margin-bottom:18px;box-shadow:8px 8px 0 var(--g,var(--p));white-space:pre-wrap;transition:.2s}
.glass:hover{transform:translate(-2px,-2px);box-shadow:10px 10px 0 var(--g,var(--p))}
.ok{box-shadow:8px 8px 0 var(--l)!important}.no{box-shadow:8px 8px 0 var(--p)!important}
.chip{display:inline-block;font-size:.72rem;font-weight:700;text-transform:uppercase;padding:3px 12px;margin:2px 6px 2px 0;border:2px solid var(--c);border-radius:99px;background:var(--k)}
.big{font-family:'Bungee';font-size:2.8rem;color:var(--l);line-height:1.1}.mut{color:#b9b4a6;font-size:.92rem}
.brand{display:flex;align-items:center;gap:10px;font-family:'Bungee';font-size:1.6rem;color:var(--c)}
.logo{background:var(--l);color:var(--k);border:3px solid var(--c);border-radius:10px;padding:0 10px;transform:rotate(-8deg);box-shadow:4px 4px 0 var(--p)}
.stButton>button,a[data-testid=stPageLink-NavLink]{background:var(--l);border:3px solid var(--k);border-radius:14px;box-shadow:5px 5px 0 var(--c);padding:.5rem 1.2rem;transition:.15s}
.stButton>button p,a[data-testid=stPageLink-NavLink] p{color:var(--k)!important;font-size:.95rem}
.stButton>button:hover,a[data-testid=stPageLink-NavLink]:hover{transform:translate(-2px,-2px);box-shadow:8px 8px 0 var(--p);background:var(--o)}
.stButton>button:active,a[data-testid=stPageLink-NavLink]:active{transform:translate(3px,3px);box-shadow:1px 1px 0 var(--c)}
div[role=radiogroup] label{background:#14141c;border:2px solid var(--c);border-radius:14px;padding:10px 14px;margin:5px 0;transition:.15s}
div[role=radiogroup] label:hover{border-color:var(--l);box-shadow:4px 4px 0 var(--l)}
.stTextArea textarea,.stSelectbox div[data-baseweb=select]>div{background:#14141c!important;border:2px solid var(--c)!important;border-radius:14px!important}
.stProgress div[role=progressbar]>div{background:var(--l)!important}
.bar{height:14px;border:2px solid var(--c);border-radius:9px;background:var(--k);overflow:hidden;margin-bottom:8px}.bar i{display:block;height:100%;background:var(--l)}
.msg{padding:10px 14px;margin:6px 0;border:2px solid var(--c);border-radius:14px;background:#14141c}.msg.Interrogator{background:#3d5aff55;margin-left:8%}.msg.stage{border-style:dashed;font-style:italic}
.mq{overflow:hidden;white-space:nowrap;border-block:3px solid var(--c);background:var(--p);color:var(--k)}.mq.g{background:var(--l)}
.mq div{display:inline-block;font-family:'Bungee';font-size:1.5rem;padding:4px 0;animation:mq 26s linear infinite}.mq.g div{animation-direction:reverse;animation-duration:34s}
.rail{display:flex;align-items:center;gap:28px;overflow-x:auto;overflow-y:hidden;height:auto;min-height:480px;padding:24px 2vw 36px 2vw;scroll-snap-type:x proximity;scrollbar-color:var(--l) #0000}
.hero{flex:0 0 min(88vw,980px);height:auto;display:flex;flex-direction:column;justify-content:center;padding:10px 0;box-sizing:border-box}
.w1{font-family:'Bungee Shade';font-size:clamp(2.8rem,min(8vw,11vh),6.2rem);line-height:1.05;color:var(--l);margin-bottom:4px}
.w2{font-family:'Bungee';font-size:clamp(1.4rem,min(3.2vw,5vh),2.6rem);color:transparent;-webkit-text-stroke:2px var(--c);line-height:1.2}
.sub{font-size:1rem;max-width:620px;margin:12px 0 16px 0;line-height:1.4}
.tile{flex:0 0 300px;height:340px;scroll-snap-align:center;display:flex;flex-direction:column;justify-content:space-between;padding:22px;background:var(--t);color:var(--tc);border:4px solid var(--k);border-radius:26px;box-shadow:10px 10px 0 var(--c);transform:rotate(var(--r,0deg));transition:.25s}
.tile:nth-child(odd){--r:-2.5deg}.tile:nth-child(even){--r:2deg}.tile:hover{transform:rotate(0) translateY(-12px) scale(1.05)}
.tn{font-family:'Bungee';font-size:4.4rem;line-height:1}.tt{font-family:'Bungee';font-size:1.45rem;line-height:1.1;margin-bottom:6px}.td{font-weight:600;font-size:.95rem}
.fit{width:100%;height:300px;margin-bottom:12px}
.sec{flex:0 0 110px;height:340px;writing-mode:vertical-rl;transform:rotate(180deg);font-family:'Bungee';font-size:2.8rem;color:transparent;-webkit-text-stroke:2px var(--c);white-space:nowrap}
.timer-box{display:flex;align-items:center;justify-content:space-between;padding:10px 18px;background:#1a1a24;border:2px solid var(--o);border-radius:14px;margin-bottom:12px;font-family:'Bungee';color:var(--o)}
.sim-grid{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0}
.sim-node{width:50px;height:50px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Bungee';font-size:1.2rem;border:3px solid var(--c);background:#14141c;color:var(--c);cursor:pointer;transition:.2s}
.sim-node.visited{background:var(--l);color:var(--k);border-color:var(--l);box-shadow:0 0 10px var(--l)}
.sim-node.frontier{background:var(--b);color:var(--c);border-color:var(--b)}
.sim-node.current{background:var(--p);color:var(--c);border-color:var(--c);transform:scale(1.15)}
</style>"""

def boot():
    st.set_page_config(page_title=f"{APP} | {TAG}", page_icon="🕵️", layout="wide", initial_sidebar_state="collapsed")
    st.markdown(CSS, unsafe_allow_html=True)

def nav():
    c = st.columns([2.4, 1, 1.3, 1.3, 1.3])
    c[0].markdown(f"<div class='brand'><span class='logo'>1</span>{APP.upper()}</div>", unsafe_allow_html=True)
    for col, (p, l) in zip(c[1:], [("app.py", "HOME"), ("pages/1_Case_Mode.py", "CASE MODE"), ("pages/2_Viva_Mode.py", "VIVA MODE"), ("pages/3_Analytics.py", "ANALYTICS")]):
        col.page_link(p, label=l)