import streamlit as st
import random
import time
import base64
from pathlib import Path

# ─── Page Configuration ───────────────────────────
st.set_page_config(page_title="🎉 Lucky Draw", layout="centered")

# ─── Caching Helpers ──────────────────────────────
@st.cache_data
def load_base64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode()

@st.cache_data
def load_participants(path: str) -> list[str]:
    text = Path(path).read_text(encoding="utf-8")
    return [line.strip() for line in text.splitlines() if line.strip()]

img_base64 = load_base64("logo.png")
participants = load_participants("namelist.txt")

# ─── Background & Header ──────────────────────────
st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
        }}
    </style>
    <h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px #000;'>Seastea 50 Give Away 🎉</h1>
""", unsafe_allow_html=True)

# ─── User Controls & Forced Winners ────────────────
num_winners = st.sidebar.slider("Number of winners", 1, min(50, len(participants)), 50)
forced = ["@nininininini2212", "@christinachoo223"]

# Sanity checks
missing = [w for w in forced if w not in participants]
if missing:
    st.error(f"Forced winners not found: {', '.join(missing)}")
    st.stop()
if num_winners < len(forced):
    st.error(f"Pick at least {len(forced)} winners to include your forced entries.")
    st.stop()

# ─── Draw Logic ───────────────────────────────────
if st.button("🎰 Start the Lucky Draw!"):
    # 1) Build the full winner sequence
    pool = participants.copy()
    for f in forced:
        pool.remove(f)
    others = random.sample(pool, num_winners - len(forced))

    # decide random slots for forced winners
    slots = list(range(num_winners))
    forced_slots = random.sample(slots, len(forced))
    random.shuffle(forced)

    sequence: list[str] = [None] * num_winners
    for slot, name in zip(forced_slots, forced):
        sequence[slot] = name

    idx_other = 0
    for i in range(num_winners):
        if sequence[i] is None:
            sequence[i] = others[idx_other]
            idx_other += 1

    # 2) Reveal one-by-one
    st.session_state.winners = []
    draw_ph = st.empty()
    list_ph = st.empty()

    for i, winner in enumerate(sequence, start=1):
        # spin animation (5 quick flashes)
        for _ in range(5):
            candidate = random.choice(pool + forced)  # just for show
            draw_ph.markdown(f"🎲 Drawing: **{candidate}**")
            time.sleep(0.05)

        # actually reveal
        st.session_state.winners.append(winner)
        draw_ph.markdown(f"🎉 Winner {i}: **{winner}**")
        list_ph.markdown("\n\n".join(
            f"{j}. **{n}**"
            for j, n in enumerate(st.session_state.winners, 1)
        ))

        time.sleep(0.5)  # 0.5 s between picks

    draw_ph.empty()
    st.balloons()
    st.success("All winners have been drawn!")

# ─── Display Past Winners ─────────────────────────
if st.session_state.get("winners"):
    st.markdown("## 🏆 Winners List")
    for idx, name in enumerate(st.session_state.winners, 1):
        st.markdown(f"{idx}. **{name}**")
