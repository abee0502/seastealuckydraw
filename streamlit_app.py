import streamlit as st
import random
import time
import base64
from pathlib import Path

# ─── Page Configuration ───────────────────────────
st.set_page_config(page_title="🎉 Lucky Draw", layout="centered")

# ─── Caching Helpers ──────────────────────────────
@st.cache_data
def load_base64(path: str) -> str | None:
    try:
        return base64.b64encode(Path(path).read_bytes()).decode()
    except Exception:
        return None

@st.cache_data
def load_participants(path: str) -> list[str]:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except Exception:
        return []
    # Deduplicate while preserving order
    seen, out = set(), []
    for line in (x.strip() for x in text.splitlines() if x.strip()):
        if line not in seen:
            seen.add(line)
            out.append(line)
    return out

img_base64 = load_base64("logo.png")
participants = load_participants("namelist.txt")

# Fail fast but with UI
if not participants:
    st.error("No participants found. Ensure **namelist.txt** exists and is not empty.")
    st.stop()

# ─── Background & Header ──────────────────────────
bg_css = f"""
<style>
    .stApp {{
        {"background-image: url('data:image/png;base64," + img_base64 + "');" if img_base64 else ""}
        background-size: cover;
        background-position: center;
    }}
</style>
"""
st.markdown(bg_css, unsafe_allow_html=True)
st.markdown(
    "<h1 style='text-align:center;color:white;text-shadow:2px 2px 4px #000'>Seastea 50 Give Away 🎉</h1>",
    unsafe_allow_html=True,
)

# ─── User Controls (Fair draw, no forced winners) ─
max_winners = min(50, len(participants))
num_winners = st.sidebar.slider("Number of winners", 1, max_winners, max_winners)

# ─── Draw Logic ───────────────────────────────────
if st.button("🎰 Start the Lucky Draw!"):
    # Sample unique winners uniformly at random
    winners = random.sample(participants, num_winners)

    # Build the reveal sequence (already random)
    sequence = winners

    # 2) Reveal one-by-one
    st.session_state.winners = []
    draw_ph = st.empty()
    list_ph = st.empty()

    for i, winner in enumerate(sequence, start=1):
        # spin animation (5 quick flashes)
        for _ in range(5):
            candidate = random.choice(participants)  # just for show
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
