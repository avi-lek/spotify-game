from helpers import *
from gameLoop import *
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

token=get_token()
print(get_names(search_for_track(token, "only")))
print(get_track_names(search_for_track(token, "only")))