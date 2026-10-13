import json, random, csv, html, pathlib, datetime, time
import streamlit as st

D = pathlib.Path(__file__).resolve().parent.parent / "data"
RT = {"easy": 900, "medium": 1100, "hard": 1300}
PT = {"easy": 10, "medium": 15, "hard": 20}
TIME_LIMITS = {"easy": 45, "medium": 60, "hard": 90}

CH = [
    ("The Interview Room", "01", "Turing Test, agents, rationality. Spot the bot.", "#8b5cf6", "#22d3ee"),
    ("The Server Floor", "02", "PEAS and the nature of environments.", "#22d3ee", "#34d399"),
    ("The Case Archive", "03", "State spaces, production systems, problem types.", "#34d399", "#fbbf24"),
    ("The Search Grid", "04", "BFS, DFS and iterative deepening.", "#fbbf24", "#fb7185"),
    ("The Heuristic Peaks", "05", "Hill climbing, best-first, CSP, means-end.", "#fb7185", "#8b5cf6")
]

esc = lambda s: html.escape(str(s))

@st.cache_data
def data():
    f = lambda n: json.load(open(D / n, encoding="utf-8"))
    return f("bank.json"), f("extras.json")

def pool(z):
    B, X = data()
    return [("q", q) for q in B if q["zone"] == z] + \
           [("bh", b) for b in X.get("bug_hunt", []) if b["zone"] == z] + \
           [("ir", r) for r in X.get("interrogation", []) if r["zone"] == z]

def new_game(mode, items, label):
    st.session_state.g = dict(
        mode=mode, label=label, left=list(items), total=len(items), cur=None,
        score=0, streak=0, elo=1000.0, log=[], fb=None, rev=False, hid=[],
        pen=0, hint=False, done=False, saved=False,
        start_time=time.time(), time_left=60, timed_out=False
    )

def advance(g):
    if not g["left"]:
        g["done"] = True
        g["cur"] = None
        return
    if g["mode"] == "case":
        g["left"].sort(key=lambda it: abs(RT.get(it[1].get("difficulty", "medium"), 1100) - g["elo"]) + random.random() * 120)
    g["cur"] = g["left"].pop(0)
    diff = g["cur"][1].get("difficulty", "medium")
    t_limit = TIME_LIMITS.get(diff, 60)
    g.update(
        fb=None, rev=False, hid=[], pen=0, hint=False,
        start_time=time.time(), time_left=t_limit, timed_out=False
    )

def finish(g, ok, msg=""):
    k, d = g["cur"]
    diff = d.get("difficulty", "medium")
    elapsed = max(1, int(time.time() - g["start_time"]))
    time_bonus = max(0, int((TIME_LIMITS.get(diff, 60) - elapsed) // 5)) if ok >= 1 else 0

    base_pts = round(ok * (PT[diff] + min(g["streak"], 5) * 2))
    pts = max(0, base_pts + time_bonus - g["pen"]) if ok else 0

    g["score"] += pts
    g["streak"] = g["streak"] + 1 if ok >= 1 else 0
    e = 1 / (1 + 10 ** ((RT[diff] - g["elo"]) / 400))
    g["elo"] += 32 * (ok - e)

    g["log"].append(dict(
        id=d["id"], zone=d["zone"], topic=d.get("topic") or d.get("algorithm"),
        kind=k if k != "q" else d["type"], diff=diff, ok=ok, elapsed=elapsed
    ))
    if ok < 1 and g["mode"] == "case" and not d.get("_rq"):
        g["left"].insert(min(3, len(g["left"])), (k, {**d, "_rq": 1}))
    bonus_str = f" (+{time_bonus}s time bonus)" if time_bonus > 0 else ""
    g["fb"] = (ok, msg, f"{pts}{bonus_str}")

def persist(g):
    if g["saved"]: return
    g["saved"] = True
    f = D / "attempts.csv"
    new = not f.exists()
    now = datetime.datetime.now().isoformat(timespec="seconds")
    with open(f, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, ["time", "mode", "id", "zone", "topic", "kind", "diff", "ok", "elapsed"])
        if new: w.writeheader()
        for r in g["log"]:
            w.writerow({"time": now, "mode": g["mode"], **r})
    lb = D / "leaderboard.json"
    rows = json.load(open(lb)) if lb.exists() else []
    rows.append(dict(
        name=st.session_state.get("name", "Auditor"),
        score=g["score"], mode=g["label"], date=now[:10]
    ))
    json.dump(sorted(rows, key=lambda r: -r["score"])[:10], open(lb, "w"), indent=2)