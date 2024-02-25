from helpers import *
import streamlit as st
from streamlit_searchbox import st_searchbox
import networkx as nx
import matplotlib.pyplot as plt
import time
import streamlit_js_eval

token=get_token()
def get_artist_terms(searchterm: str) -> list[any]:
    if searchterm:
        return get_names(search_for_artist(token, searchterm)) 
def get_music_terms(searchterm: str) -> list[any]:
    if searchterm:
        return get_track_names(search_for_track(token, searchterm)) 
def make_searchbox(term_function, key):
    selected_value = st_searchbox(term_function, key=key)
    return selected_value
def visualize_graph(graph):
    pos = nx.spring_layout(graph, scale=2)
    nx.draw(graph, pos, with_labels=True, font_weight='bold', node_size=700, font_size=8)
    edge_labels = nx.get_edge_attributes(graph,'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
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
    for component in nx.connected_components(graph):
        if st.session_state["artist1"] in component and st.session_state["artist2"] in component:
            return True
    return False

def is_node_unconnected(graph, node):
    components = list(nx.connected_components(graph))
    for component in components:
        if node in component and len(component)>=2:
            return False
    return True

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
        if is_node_unconnected(st.session_state["graph"], list(st.session_state["graph"].nodes())[-1]):
            st.session_state["graph"].remove_node(list(st.session_state["graph"].nodes())[-1])  
        if is_node_unconnected(st.session_state["graph"], list(st.session_state["graph"].nodes())[-1]):
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

def shorten_track_name(track_name):
    return track_name[0:track_name.rindex(" - ")]

def game_round(a1, a2):
    #Create Graph
    if "graph" not in st.session_state:
        st.session_state["graph"] = nx.Graph()

    #Create Delete Button, Add Song, and Add Artist
    with st.sidebar:
        st.write("To win, link " + a1 + " and " + a2 + " through features.")
        if st.button("DELETE LAST TRACK", key="b2"):
            delete_node(st.session_state["graph"])  
        song = make_searchbox(get_music_terms, "s3")
        
    if str(type(song))!="<class 'NoneType'>" and song not in list(st.session_state["graph"].nodes()):
        new_nodes=select_artists_from_track(song)
        if len(new_nodes)==2:
            st.session_state["graph"].add_node(new_nodes[0])
            st.session_state["graph"].add_node(new_nodes[1])
            st.session_state["graph"].add_edge(new_nodes[0], new_nodes[1], label=shorten_track_name(song))


    visualize_graph(st.session_state["graph"])
    if check_win(st.session_state["graph"], st.session_state["artist1"], st.session_state["artist2"]):
            st.success("YOU WIN!!!")
            if st.sidebar.button("PLAY AGAIN"):
                clear_cache()
                streamlit_js_eval.streamlit_js_eval(js_expressions="parent.window.location.reload()")
            


def clear_cache():
    for key in st.session_state.keys():
        del st.session_state[key]


