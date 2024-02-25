from helpers import *
import graphviz
import streamlit as st
from streamlit_searchbox import st_searchbox
import networkx as nx
import matplotlib.pyplot as plt
import time

token=get_token()
def get_artist_terms(searchterm: str) -> list[any]:
    if searchterm:
        return get_names(search_for_artist(token, searchterm)) 
def get_music_terms(searchterm: str) -> list[any]:
    if searchterm:
        #return get_names(search_for_track(token, searchterm)) 
        return get_track_names(search_for_track(token, searchterm)) 
def make_searchbox(term_function, key):
    selected_value = st_searchbox(term_function, key=key)
    return selected_value

def makeGraph():
    graph = graphviz.Graph()
    return graph

def visualize_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, font_weight='bold')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

def delete_session():
    for key in st.session_state.keys():
        del st.session_state[key]

def choose_artists():
    if "artist1" not in st.session_state or "artist2" not in st.session_state:
        pregame = st.sidebar.empty()
        with pregame.container():
            st.write("Artist 1:")
            artist1 = make_searchbox(get_artist_terms, "s1")
            st.write()
            st.write("Artist 2:")
            artist2 = make_searchbox(get_artist_terms, "s2")
            if st.button("START GAME", key="b1"):
                if str(type(artist1))!="<class 'NoneType'>" and str(type(artist2))!="<class 'NoneType'>":
                    pregame.empty()
                    st.session_state["artist1"]=artist1
                    st.session_state["artist2"]=artist2

def check_win(graph, a1, a2):
    if len(list(graph.nodes()))<2:
        return False
    if list(graph.nodes())[0]==a1 and list(graph.nodes())[-1]==a2:
        delete_session()
        return True
    elif list(graph.nodes())[-1]==a1 and list(graph.nodes())[0]==a2:
        delete_session()
        return True
    else:
        return False

def delete_node(graph):
    if len(list(st.session_state["graph"].nodes()))==0:
        placeholder = st.empty()
        with placeholder.container():
            st.warning('Cannot Delete Link If Web Is Empty', icon="⚠️")
            time.sleep(1)
            placeholder.empty()
    elif len(list(st.session_state["graph"].nodes()))==1:
        st.session_state["graph"].remove_node(list(st.session_state["graph"].nodes())[-1])
    else:
        st.session_state["graph"].remove_edge(*(list(st.session_state["graph"].edges())[-1]))
        st.session_state["graph"].remove_node(list(st.session_state["graph"].nodes())[-1])

#select artists from a track
def select_artists_from_track(song):
    track_info = search_for_track(token, song)[0]
    artists = [n["name"] for n in track_info["artists"]]
    if len(artists)>=2:
        selected_artists = st.sidebar.multiselect("Select two artists from " + song + ":", artists, max_selections=2)
        if len(selected_artists)>=2:
            return selected_artists
        else:
            return []
    else:
        return []

def game_round(a1, a2):
    #Create Graph
    if "graph" not in st.session_state:
        st.session_state["graph"] = nx.Graph()

    #Create Delete Button, Add Song, and Add Artist
    with st.sidebar:
        if st.button("DELETE LAST CHANGE", key="b2"):
            delete_node(st.session_state["graph"])  
        song = make_searchbox(get_music_terms, "s3")
        
    if str(type(song))!="<class 'NoneType'>" and song not in list(st.session_state["graph"].nodes()):
        x=select_artists_from_track(song)
        st.write(x)
        if len(x)>=2:
            st.session_state["graph"].add_node(song)
            if len(st.session_state["graph"].nodes())>=2:
                st.session_state["graph"].add_edge(list(st.session_state["graph"].nodes())[-2], song)

    visualize_graph(st.session_state["graph"])
    if check_win(st.session_state["graph"], st.session_state["artist1"], st.session_state["artist2"]):
            st.success("YOU WIN")

