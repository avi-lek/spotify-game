#pip install python-dotenv
#pip install requests
#pip install streamlit
#pip install graphviz
#pip install streamlit-searchbox

from helpers import *
from gameLoop import *
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt


st.set_page_config(layout="wide", page_title="Spotify Game")
choose_artists()
if "artist1" in st.session_state and "artist2" in st.session_state and len(st.session_state["artist1"])>0 and len(st.session_state["artist2"])>0:
    game_round(st.session_state["artist1"], st.session_state["artist2"])






#artist = search_for_artist(token, "Montero")
#print(artist[0]["album"]["images"])

#print(type(artist[0]["external_urls"]))
#print(artist[1]["name"])
#print(artist[2]["name"])
#name = st.text_input("Music Artist Name")
#if len(name)!=0:
    #artist = search_for_artist(token, name)
    #st.title(artist[0]["name"])
    #st.image(artist[0]["images"][0]["url"])
    #st.image(artist[0]["images"][0]["url"], width=100)

