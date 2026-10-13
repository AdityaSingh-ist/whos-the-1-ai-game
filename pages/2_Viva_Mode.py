import random
import streamlit as st
from core.theme import boot, nav
from core.engine import data, new_game
from core.ui import play, card
boot(); nav()
st.session_state.setdefault("name", "Auditor")
g = st.session_state.get("g")
if g and g["mode"] == "viva": play(g)
else:
    st.markdown("<h1 class='grad'>Viva Mode</h1>", unsafe_allow_html=True)
    card("Ten random questions, exactly like the class viva. No options are shown: answer in your own words, reveal the model answer, then rate yourself. Your weak-topic radar appears at the end.", "#fbbf24")
    st.text_input("Auditor name", key="name")
    if st.button("Begin the examination"):
        B, _ = data(); new_game("viva", [("q", q) for q in random.sample([q for q in B if q["type"] != "MATCH"], 10)], "Viva Mode"); st.rerun()
