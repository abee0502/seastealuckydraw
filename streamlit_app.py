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

# ─── Draw Logic ───────────────────────────────────
if participants and st.button("🎰 Start the Lucky Draw!"):
    available = participants.copy()
    st.session_state.winners = []
    current_draw = st.empty()
    winners_list = st.empty()

    for i in range(num_winners):
        if not available:
            st.warning("⚠️ Not enough participants!")
            break

        # Optional spin animation
        for _ in range(10):
            candidate = random.choice(available)
            current_draw.markdown(f"🎲 Drawing: **{candidate}**")
            time.sleep(0.1)

        # Final pick
        winner = random.choice(available)
        available.remove(winner)
        st.session_state.winners.append(winner)

        # Update displays
        current_draw.markdown(f"🎉 Winner {i+1}: **{winner}**")
        winners_list.markdown("\n\n".join(
            f"{idx+1}. **{name}**"
            for idx, name in enumerate(st.session_state.winners)
        ))

        time.sleep(2)

    current_draw.empty()
    st.balloons()
    st.success("All winners have been drawn!")

# ─── Display Past Winners ─────────────────────────
if st.session_state.get("winners"):
    st.markdown("## 🏆 Winners List")
    for idx, name in enumerate(st.session_state.winners, 1):
        st.markdown(f"{idx}. **{name}**")
