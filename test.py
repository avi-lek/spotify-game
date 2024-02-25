from helpers import *
from gameLoop import *
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.session_state["graph"] = nx.Graph()

st.session_state["graph"].add_node("n1")
st.session_state["graph"].add_node("n2")
st.session_state["graph"].add_node("n3")
st.session_state["graph"].add_edge('n1', 'n2', label='track1')
st.session_state["graph"].add_edge('n3', 'n2', label='track2')



