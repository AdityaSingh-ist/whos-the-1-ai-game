import streamlit as st
from core.theme import boot, nav
from core.engine import CH, pool, new_game
from core.ui import play

boot()
nav()

st.session_state.setdefault("name", "Auditor")
g = st.session_state.get("g")
COL = ["#c6ff2e", "#ff3d8b", "#3d5aff", "#ff8a1f", "#fff4e0"]

# Strict separation: Only show the game (and timer) if mode is "case"
if g and g["mode"] == "case": 
    play(g)
else:
    # Render the exact Main Menu you are supposed to see
    st.markdown("<h1 class='grad' style='margin-top:0'>PICK A CHAPTER</h1>", unsafe_allow_html=True)
    st.text_input("Auditor name", key="name")
    
    cols = st.columns(5)
    for i, (col, (n, ic, d, *_)) in enumerate(zip(cols, CH), 1):
        tc = "#fff4e0" if COL[i - 1] == "#3d5aff" else "#0d0d12"
        col.markdown(f"<div class='tile fit' style='--t:{COL[i-1]};--tc:{tc}'><div class='tn'>{ic}</div><div><div class='tt'>{n.upper()}</div><div class='td'>{d} {len(pool(i))} files.</div></div></div>", unsafe_allow_html=True)
        if col.button("ENTER", key=f"c{i}"): 
            new_game("case", pool(i), n)
            st.rerun()