from src.get_song import get_similar_song
import pprint

song = False
artist = False
E = True 

print("To skip any input press enter ")
while True:
    song= input("enter song name : ")
    artist= input("enter artist name : ")
    result = get_similar_song(song_name=song, artist_name=artist, Explicit=E)
    pprint.pprint(result)
