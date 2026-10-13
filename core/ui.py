import random, time
import streamlit as st
import streamlit.components.v1 as components
from core.engine import *

TXT = ("FIB", "SCENARIO", "PROBLEM")

def card(h, c="#3d5aff", cls=""): 
    st.markdown(f"<div class='glass {cls}' style='--g:{c}'>{h}</div>", unsafe_allow_html=True)

def chips(*t): 
    return "".join(f"<span class='chip'>{esc(x)}</span>" for x in t)

def radar(log):
    import plotly.graph_objects as go
    v = [sum(l["ok"] for l in log if l["zone"] == z) / max(1, sum(1 for l in log if l["zone"] == z)) * 100 for z in range(1, 6)]
    fig = go.Figure(go.Scatterpolar(
        r=v + v[:1], theta=[f"Ch {i}" for i in range(1, 6)] + ["Ch 1"], 
        fill="toself", line_color="#c6ff2e", fillcolor="rgba(198,255,46,.35)"
    ))
    fig.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(range=[0, 100], gridcolor="#ffffff33")), 
        paper_bgcolor="rgba(0,0,0,0)", font_color="#fff4e0", margin=dict(t=20, b=20), height=320
    )
    return fig

def result(g):
    persist(g)
    L = g["log"]
    a = round(100 * sum(l["ok"] for l in L) / max(1, len(L)))
    el = round(g["elo"])
    card(f"<div class='mut'>CASE REPORT · {esc(g['label'])}</div><div class='big grad'>{g['score']} pts</div>" + 
         chips(f"Accuracy {a}%", f"Rating {el}", f"{len(L)} files"), "#c6ff2e")
    c1, c2 = st.columns(2)
    c1.plotly_chart(radar(L), use_container_width=True)
    t = {}
    for l in L: t.setdefault(l["topic"], []).append(l["ok"])
    w = sorted(((k, sum(v) / len(v)) for k, v in t.items() if sum(v) < len(v)), key=lambda x: x[1])[:5]
    c2.markdown("<div class='glass'><b>Revise these topics</b>" + 
                "".join(f"<div class='mut'>{esc(k)}</div><div class='bar'><i style='width:{int(v*100)}%'></i></div>" for k, v in w) + 
                ("" if w else "<br>Clean sweep.") + "</div>", unsafe_allow_html=True)
    if st.button("New run"): 
        del st.session_state["g"]
        st.rerun()

def render_timer_ui(rem, key):
    c1, c2 = st.columns([3, 1])
    with c2:
        st.markdown(f"<div class='timer-box'><span>⏱ REMAINING</span><span id='time-val-{key}'>{rem}s</span></div>", unsafe_allow_html=True)
        
    js = f"""
    <script>
    const doc = window.parent.document;
    const el = doc.getElementById('time-val-{key}');
    if (el) {{
        if (window.activeQuizTimer) clearInterval(window.activeQuizTimer);
        let r = {rem};
        window.activeQuizTimer = setInterval(() => {{
            r--;
            if (r <= 0) {{
                el.innerText = '0s';
                clearInterval(window.activeQuizTimer);
            }} else {{
                if (doc.contains(el)) {{
                    el.innerText = r + 's';
                }} else {{
                    clearInterval(window.activeQuizTimer);
                }}
            }}
        }}, 1000);
    }}
    </script>
    """
    components.html(js, height=0)

def render_search_simulator(d, key):
    sim = d.get("sim_data")
    if not sim: return
    with st.expander("🛠 OPEN INTERACTIVE SEARCH SIMULATOR", expanded=True):
        st.markdown("<b>Trace Visualizer:</b> Click through the step-by-step expansion state or run step verification:")
        if "expansion_order" in sim:
            steps = sim["expansion_order"]
            step_idx = st.slider("Step through Expansion Order", 1, len(steps), 1, key=f"sim_step_{key}")
            cur_node = steps[step_idx - 1]
            visited = steps[:step_idx]

            st.write(f"**Step {step_idx}**: Visiting **{cur_node}** | Explored set: `{visited}`")
            cols = st.columns(len(steps))
            for i, node in enumerate(steps):
                state_cls = "current" if node == cur_node else ("visited" if node in visited else "")
                cols[i].markdown(f"<div class='sim-node {state_cls}'>{node}</div>", unsafe_allow_html=True)

        elif "terrain_heights" in sim:
            th = sim["terrain_heights"]
            st.line_chart(th)
            st.caption(f"Start Index: {sim.get('start_index')} | Global Peak: {sim.get('global_maximum')}")

def play(g):
    if g["cur"] is None and not g["done"]: advance(g)
    if g["done"]: return result(g)
    
    k, d = g["cur"]
    n = g["total"] - len(g["left"])
    viva = g["mode"] == "viva"
    key = d["id"] + str(d.get("_rq", 0))

    diff = d.get("difficulty", "medium")
    limit = TIME_LIMITS.get(diff, 60)
    elapsed = int(time.time() - g["start_time"])
    rem = max(0, limit - elapsed)

    if rem <= 0 and not g["fb"]:
        g["timed_out"] = True
        finish(g, 0, "Time expired! A forensic auditor needs rapid response under crisis.")
        st.rerun()

    if not g["fb"]:
        render_timer_ui(rem, key)
    
    card(chips(g["label"], f"File {n}/{g['total']}", f"Score {g['score']}", f"Streak {g['streak']}", f"Rating {round(g['elo'])}"))
    
    # FIX: Safely clamp the progress bar between 0.0 and 1.0 to prevent StreamlitAPIException
    progress_val = max(0.0, min(1.0, (n - 1) / max(1, g["total"])))
    st.progress(progress_val)

    if k == "q":
        # If in Viva mode, change the tag so it doesn't confusingly say "MCQ"
        display_type = "OPEN-ENDED" if viva else d["type"]
        card(chips(display_type, d["topic"], d["difficulty"]) + f"<br><b style='font-size:1.15rem'>{esc(d['question'])}</b>")
        if d.get("sim_data"):
            render_search_simulator(d, key)
            
    elif k == "bh":
        prob = esc("; ".join(f"{a}: {b}" for a, b in d["problem"].items() if a != "adjacency"))
        card(chips("Bug Hunt", d["algorithm"]) + f"<br><b>{esc(d['story_intro'])}</b><br><span class='mut'>{esc(d['rules'])}</span><br><code>{prob}</code><br>Find the ONE wrong line.")
        
    else:
        tr = "".join(f"<div class='msg {m['speaker']}'><b>{'' if m['speaker'] == 'stage' else esc(m['speaker']) + ': '}</b>{esc(m['text'])}</div>" for m in d["transcript"])
        card(chips("Interrogation Room") + f"<br><b>{esc(d['story_intro'])}</b>{tr}Who is the bot?")

    if g["fb"]:
        ok, msg, pts = g["fb"]
        head = "Correct" if ok >= 1 else "Partly" if ok else "Not quite"
        card(f"<b>{head}  +{pts}</b>\n{esc(msg)}", "#c6ff2e" if ok >= 1 else "#ff3d8b", "ok" if ok >= 1 else "no")
        if st.button("Next file →"): 
            advance(g)
            st.rerun()
        return

    if k == "q" and (viva or d["type"] in TXT):
        st.text_area("Your answer (write it first, like in the viva)", key="t" + key, height=110)
        if not g["rev"]:
            if st.button("Reveal model answer"): 
                g["rev"] = True
                st.rerun()
        else:
            ex = f"\n\n<b>Examiner may ask:</b> {esc(d['viva_followup'])}" if viva else ""
            card(f"<b>Model answer:</b> {esc(d['answer'])}\n\n{esc(d['explanation'])}{ex}", "#ff8a1f")
            for col, (lab, v) in zip(st.columns(3), [("Got it", 1), ("Partly", .5), ("Missed", 0)]):
                if col.button(lab, key=f"{lab}{key}"): 
                    finish(g, v, "")
                    st.rerun()
        return

    if k == "q" and d["type"] in ("MCQ", "AR", "TF"):
        opts = ["True", "False"] if d["type"] == "TF" else [o for o in d["options"] if o[0] not in g["hid"]]
        v = st.radio("Your answer", opts, index=None, key="r" + key)
        c = st.columns(3)
        if d["type"] != "TF" and c[0].button("Narrow Suspects"):
            g["hid"] = [o[0] for o in random.sample([o for o in d["options"] if o[0] != d["answer"]], 2)]
            st.rerun()
        if c[1].button("Ask the Lab Tech"): 
            g["pen"] = 2
            g["hint"] = True
        if c[2].button("Reopen Later"): 
            g["left"].append(g["cur"])
            advance(g)
            st.rerun()
            
        if g["hint"]: 
            card("Lab Tech: " + esc(d["hint"]), "#ff8a1f")
            
        if st.button("Lock in answer", disabled=v is None):
            ok = int(v == d["answer"] or v[0] == d["answer"])
            finish(g, ok, d["explanation"] + ("" if ok else f"\nCorrect answer: {d['answer']}"))
            st.rerun()

    elif k == "q":  
        sel = [st.selectbox(l, ["-"] + d["right"], key=f"m{i}{key}") for i, l in enumerate(d["left"])]
        if st.button("Lock in answer"):
            ans = [p.strip()[-1] for p in d["answer"].split(", ")]
            ok = int(len(ans) == len(sel) and all(s[0] == ans[i] for i, s in enumerate(sel)))
            finish(g, ok, d["explanation"] + "\nCorrect: " + d["answer"])
            st.rerun()

    elif k == "bh":
        v = st.radio("Which line is wrong?", [s["n"] for s in d["steps"]], index=None, format_func=lambda n: f"{n}. {d['steps'][n-1]['text']}", key="b" + key)
        if st.button("Flag this line", disabled=v is None): 
            finish(g, int(v == d["wrong_step"]), f"{d['error_type']}. {d['why_wrong']}\nCorrect line: {d['corrected_step']}\nViva: {d['viva_followup']}")
            st.rerun()

    else:
        v = st.radio("The bot is...", ["A", "B"], index=None, key="i" + key)
        cc = d["concept_check"]
        if st.button("Accuse", disabled=v is None):
            finish(g, int(v == d["bot"]), d["verdict"] + "\nGiveaways: " + "; ".join(d["tells"]) + f"\n\nConcept check: {cc['question']} {cc['answer']}. {cc['explanation']}\nViva: {d['viva_followup']}")
            st.rerun()