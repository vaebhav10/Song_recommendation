from pathlib import Path

import streamlit as st

from src.get_song import get_similar_song

BASE_DIR = Path(__file__).resolve().parent

st.title("Song Recommendation dashboard")
st.caption("Get recommendations using both/none/either song and artist name ")


Song, Artist = st.columns([5, 5])

with Song:
    Song = st.text_input("Song", placeholder="Enter song name ")

with Artist:
    Artist = st.text_input("Aritist", placeholder="Enter aritst name ")

allow_explicit = not st.checkbox("Exclude Eplicit songs")

if st.button("Get recommendations"):
    result = get_similar_song(
        song_name=Song, artist_name=Artist, Explicit=allow_explicit
    )
    if result is False:
        st.warning("No song found( try with different song/artist ) ")
    else:
        for i, r in result.iterrows():
            col1, col2 = st.columns([2, 8])
            with col1:
                st.link_button("spotify link", r["link"])
            with col2:
                st.markdown(r["Song"])
                st.caption(r["Artist(s)"])
                st.markdown("---")
