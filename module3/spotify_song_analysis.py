import pandas as pd
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import normalize
import numpy as np

df = pd.read_csv('Module_3_Spotify.csv', index_col= 'track_name')

all_notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
note_map = {}
i = 1
for note in all_notes:
  sharp_note = note + '#'
  note_map.update({note : i})
  note_map.update({sharp_note: i + .5})
  i+= 1
df['key_num'] = df['key'].map(note_map)
df['mode_verif'] = df['mode'].map({'Major': 1, 'Minor': 0})

df = df.dropna(subset=['bpm', 'key_num', 'mode_verif'])
i = 0
songs = df[['released_year', 'bpm', 'key_num', 'mode_verif','streams']]
songs.drop(['Love Grows (Where My Rosemary Goes)'], inplace= True)
stream_counts = songs['streams'].to_numpy()

i = 0
for value in stream_counts:
  stream_counts[i] = int(value)
  i += 1

avg_streams = sum(stream_counts)/len(stream_counts)
print('')
print('Average Amount of Streams:' + str(avg_streams))
print('Median Amount of Streams:' + str(np.median(stream_counts)))
songs = songs[['released_year', 'bpm', 'key_num', 'mode_verif']]
songs_normalized =  normalize(songs, norm = 'l1', axis = 1)

def similarity_find(target_song_name):
  print(target_song_name)
  print('streams: ' + str(df.loc[target_song_name]['streams']))
  print('')
  target_song = songs_normalized[songs.index==target_song_name].reshape(1,-1)
  euclidean_distances = pairwise_distances(target_song, songs_normalized, metric='euclidean')[0]

  euclidean_top_5_indices = euclidean_distances.argsort()[:10]
  stream_counts = []
  for i in euclidean_top_5_indices:
    if songs.index[i] == target_song_name:
      continue
    print(songs.index[i])
    print('   distance: ' + str(euclidean_distances[i]))
    print('   streams: ' + str(df.loc[songs.index[i]]['streams']))
    stream_counts.append(int(df.loc[songs.index[i]]['streams']))
  avg_streams = sum(stream_counts)/len(stream_counts)
  print('')
  print('average streams of subset:' +str(avg_streams))
    
    
print(' ')
similarity_find('Blinding Lights')
print('')
print('')
similarity_find('Shape of You')
print('')
print('')
similarity_find('Someone You Loved')
print('')
print('')
similarity_find('Dance Monkey')
print('')
print('')
similarity_find('Sunflower - Spider-Man: Into the Spider-Verse')
