import streamlit as st
import random
import time
import base64
from pathlib import Path

# ─── Page Configuration ───────────────────────────
st.set_page_config(page_title="🎉 Lucky Draw", layout="centered")

def get_base64_image(image_path):
    img_bytes = Path(image_path).read_bytes()
    return base64.b64encode(img_bytes).decode()

img_base64 = get_base64_image("logo.png")

# ─── Background Image and Title ───────────────────
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

# ─── Load Participants from File ───────────────────
with open("namelist.txt", "r", encoding="utf-8") as f:
    participants = [line.strip() for line in f if line.strip()]

# ─── Draw Logic ───────────────────────────────────
if participants:
    if 'winners' not in st.session_state:
        st.session_state.winners = []

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <style>
                div.stButton > button:first-child {
                    background-color: #FF4B4B;
                    color: white;
                    font-size: 18px;
                    border-radius: 8px;
                    padding: 0.5em 2em;
                    border: none;
                    transition: 0.3s;
                }
                div.stButton > button:first-child:hover {
                    background-color: #FF1C1C;
                    transform: scale(1.05);
                }
            </style>
        """, unsafe_allow_html=True)
        if st.button("🎰 Start the Lucky Draw!"):
            st.session_state.winners = []
            available = participants.copy()
            placeholder = st.empty()

            for i in range(50):
                if not available:
                    st.warning("⚠️ Not enough participants to draw 50 unique winners!")
                    break

                # Animate with spinning names
                for _ in range(20):
                    name = random.choice(available)
                    placeholder.markdown(f"""
                        <div style='
                            text-align:center;
                            font-size:28px;
                            color: white;
                            background: linear-gradient(90deg, #FFAA00, #FF4B4B);
                            padding: 10px;
                            border-radius: 10px;
                            box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
                            margin: 10px 0;
                        '>
                        🎲 Drawing: <strong>{name}</strong>
                        </div>
                    """, unsafe_allow_html=True)
                    time.sleep(0.07)

                winner = random.choice(available)
                available.remove(winner)
                st.session_state.winners.append(winner)

            placeholder.empty()
            st.balloons()
            st.success("🎉 Draw complete! Scroll down to see the winners.")

# ─── Display Winners ──────────────────────────────
if st.session_state.get("winners"):
    st.markdown("## 🏆 Winners List")
    st.markdown("<hr>", unsafe_allow_html=True)
    for idx, name in enumerate(st.session_state.winners, 1):
        st.markdown(f"<div style='font-size:20px; padding: 4px 0;'>{idx}. <strong>{name}</strong></div>", unsafe_allow_html=True)
