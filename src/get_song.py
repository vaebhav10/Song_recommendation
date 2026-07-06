from pathlib import Path 
import numpy as np 
import pandas as pd 
import re
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent

df = joblib.load(BASE_DIR/'utils/df.pkl')
merged = np.load(BASE_DIR/'utils/merged_mat.npy')


def get_similar_song(song_name = None, artist_name = None, Explicit = True):
    result = []
    track = song_name
    
    if  artist_name.strip():
        artist_name = artist_name.lower().strip()
        artist_name = df['artists'].apply(lambda a : artist_name in a )
    else :
        artist_name = pd.Series(True, index=df.index)
        
    if song_name.strip():
        song_name = song_name.lower().strip()
        song_name = df['track_name'].str.contains(rf"\b{re.escape(song_name)}\b",regex=True)
    else:
        song_name = pd.Series(True, index=df.index)
        
    # Indexing and song extraction 
    res = song_name & artist_name 
        
    if not res.any():
        return False
    
    if not track:
        query_mat = merged[res].mean(axis=0)
    else:
        song_ind = df[res].index[0]
        query_mat = merged[song_ind]
    
    score = np.argsort(query_mat.reshape(1,-1)@ merged.T).flatten()[::-1]
    
    for i in score:
        if not Explicit :
            if df.iloc[i]['explicit']:
                continue
        sng = df.iloc[i]['track_name']
        if sng == track: # skipping the querry song
            continue
        
        art = df.iloc[i]['artists'] 
        link = df.iloc[i]['track_id']
        link = f"https://open.spotify.com/track/{link}?autoplay_ok=1"
        if ((sng,art)) not in result:
            result.append((link, sng, art))
        if len(result)==10:
            break
    
    result =  [result[i] for i in (np.random.choice(10, replace = False, size = 5 ))]
    result = pd.DataFrame(result, columns = ['link', "Song", "Artist(s)"])
    return result