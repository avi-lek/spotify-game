from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import streamlit as st
load_dotenv()
client_id=st.secrets["CLIENT_ID"]#os.getenv("CLIENT_ID")
client_secret=st.secrets["CLIENT_SECRET"]#os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id+":"+client_secret
    auth_bytes=auth_string.encode("utf-8")
    auth_base64=str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " +  auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data={"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result=json.loads(result.content)
    token=json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token }

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=10"
    query_url=url+query
    result=get(query_url, headers=headers)
    json_result=json.loads(result.content)['artists']['items']
    if len(json_result)<=0:
        return("NO ARTIST FOUND")
    return json_result

def search_for_track(token, track_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=10"
    query_url=url+query
    result=get(query_url, headers=headers)
    json_result=json.loads(result.content)['tracks']['items']
    if len(json_result)<=0:
        return("NO TRACK FOUND")
    return json_result

def get_names(result):
    return [r["name"] for r in result]

def get_track_names(result):
    track_names = []
    for track in result:
        track_name = track["name"]
        artists = [n["name"] for n in track["artists"]]
        track_names.append(track_name + " - " + ', '.join(artists))
    return track_names
