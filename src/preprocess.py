import numpy as np 
import pandas as pd 
from pathlib import Path 
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import StandardScaler, normalize
import joblib



model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
sc = StandardScaler()

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(BASE_DIR/'data/dataset.csv')
df=df.dropna()
df.drop_duplicates(subset= ['track_id','artists', 'track_name','explicit'],inplace= True)

df.drop(columns = {'Unnamed: 0','popularity', 'duration_ms', 'album_name'}, inplace = True)

data = ['danceability','energy','key',	'loudness','mode',	'speechiness', 'acousticness', 'instrumentalness',	'liveness',	'valence',	'tempo',	'time_signature']
meta_data = df[data]
df.drop(columns = data ,inplace =True)

for col in df.select_dtypes(include = ['str']).columns:
    if col =='track_id':
        continue
    df[col] = df[col].str.strip().str.lower()
    
df['tags'] = df['artists']+ ' ' +df['track_genre']

df[df.duplicated(subset=[ 'track_name','tags','explicit'])]

df = df.reset_index(drop=True)

tag_embeddings = model.encode(df['tags'].tolist(), normalize_embeddings = True)

audio_data = sc.fit_transform(meta_data)
audio_data = normalize (audio_data)

merged = np.concatenate([audio_data, tag_embeddings], axis = 1)
merged = normalize(merged)
np.save(BASE_DIR/'utils/merged_mat.npy',merged)
# joblib.dump(df,BASE_DIR/'utils/df.pkl')

