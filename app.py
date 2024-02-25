from gameLoop import *
import streamlit as st

st.set_page_config(layout="wide", page_title="Spotify Game")
choose_artists()
if "artist1" in st.session_state and "artist2" in st.session_state and len(st.session_state["artist1"])>0 and len(st.session_state["artist2"])>0:
    game_round(st.session_state["artist1"], st.session_state["artist2"])






