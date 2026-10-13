import json
import pandas as pd
import streamlit as st
from core.theme import boot, nav
from core.engine import CH, D
boot(); nav()
st.markdown("<h1 class='grad'>Analytics</h1>", unsafe_allow_html=True)
f, lb = D / "attempts.csv", D / "leaderboard.json"
df = pd.read_csv(f) if f.exists() else pd.DataFrame(columns=["zone", "ok"])
c1, c2 = st.columns(2)
bars = "".join(f"<div class='mut'>{n} ({int((df.zone == i).sum())} attempts)</div><div class='bar'><i style='width:{int(100 * df[df.zone == i].ok.mean()) if (df.zone == i).any() else 0}%'></i></div>" for i, (n, *_) in enumerate(CH, 1))
c1.markdown(f"<div class='glass'><b>Mastery by chapter</b>{bars}</div>", unsafe_allow_html=True)
rows = json.load(open(lb)) if lb.exists() else []
board = "".join(f"<div class='msg'>{i}. {r['name']} · <b>{r['score']}</b> · {r['mode']} · {r['date']}</div>" for i, r in enumerate(rows, 1)) or "<div class='mut'>No runs yet.</div>"
c2.markdown(f"<div class='glass'><b> Leaderboard</b>{board}</div>", unsafe_allow_html=True)
if len(df): st.download_button("Export analytics CSV", df.to_csv(index=False), "whos_the_1_analytics.csv")
