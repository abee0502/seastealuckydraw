import streamlit as st
import random
import time
import base64
from pathlib import Path

st.set_page_config(page_title="🎉 Lucky Draw", layout="centered")

@st.experimental_memo
def load_base64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()

img_base64 = load_base64("logo.png")

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

participants = load_participants("namelist.txt")  # same as before

# Let user choose how many winners (optional)
num_winners = st.sidebar.slider("Number of winners", 1, min(50, len(participants)), 50)

if participants and st.button("🎰 Start the Lucky Draw!"):
    available = participants.copy()
    st.session_state.winners = []
    current_draw = st.empty()    # placeholder for the 2s display
    winners_list = st.empty()    # placeholder for the cumulative list

    for i in range(num_winners):
        if not available:
            st.warning("⚠️ Not enough participants!")
            break

        # (Optional) spin animation before final pick
        for _ in range(10):
            name = random.choice(available)
            current_draw.markdown(f"🎲 Drawing: **{name}**")
            time.sleep(0.1)

        # actual winner
        winner = random.choice(available)
        available.remove(winner)
        st.session_state.winners.append(winner)

        # update placeholders
        current_draw.markdown(f"🎉 Winner {i+1}: **{winner}**")
        winners_list.markdown("\n\n".join(
            f"{idx+1}. **{name}**" for idx, name in enumerate(st.session_state.winners)
        ))

        time.sleep(2)  # <-- pause 2 seconds before next draw

    current_draw.empty()
    st.balloons()
    st.success("All winners have been drawn!")

# display any existing winners outside the loop
if st.session_state.get("winners"):
    st.markdown("## 🏆 Winners List")
    for idx, name in enumerate(st.session_state.winners, 1):
        st.markdown(f"{idx}. **{name}**")
