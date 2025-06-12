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

# ─── User Controls ─────────────────────────────────
num_winners = st.sidebar.slider(
    "Number of winners", 1, min(50, len(participants)), 50
)

# ─── Forced winners ────────────────────────────────
forced = ["nininininini2212", "christinachoo223"]
missing = [w for w in forced if w not in participants]
if missing:
    st.error(f"The following forced winners are not in your list: {', '.join(missing)}")
    st.stop()
elif num_winners < len(forced):
    st.error(f"You must pick at least {len(forced)} winners to include the forced entries.")
    st.stop()

# ─── Draw Logic ───────────────────────────────────
if st.button("🎰 Start the Lucky Draw!"):
    available = participants.copy()
    st.session_state.winners = []

    # 1) Pre-assign the forced winners
    for w in forced:
        st.session_state.winners.append(w)
        available.remove(w)

    # placeholders for live updates
    current_draw = st.empty()
    winners_list = st.empty()

    # 2) Draw the remaining slots
    to_draw = num_winners - len(forced)
    for i in range(to_draw):
        # quick “spin” (shorter & fewer steps)
        for _ in range(5):
            candidate = random.choice(available)
            current_draw.markdown(f"🎲 Drawing: **{candidate}**")
            time.sleep(0.05)

        winner = random.choice(available)
        available.remove(winner)
        st.session_state.winners.append(winner)

        # update UI
        current_draw.markdown(f"🎉 Winner {len(st.session_state.winners)}: **{winner}**")
        winners_list.markdown("\n\n".join(
            f"{idx+1}. **{name}**"
            for idx, name in enumerate(st.session_state.winners)
        ))

        # pause only half a second
        time.sleep(0.5)

    current_draw.empty()
    st.balloons()
    st.success("All winners have been drawn!")

# ─── Display Past Winners ─────────────────────────
if st.session_state.get("winners"):
    st.markdown("## 🏆 Winners List")
    for idx, name in enumerate(st.session_state.winners, 1):
        st.markdown(f"{idx}. **{name}**")
