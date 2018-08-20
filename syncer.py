import json
from pprint import pprint
import sys
import spotipy
import spotipy.util as util


class SpotifyConn:
    
    def __init__(self, username):
        self.username = username

        # Init Conn
        self.sp = self.init_conn(self.username)
        self.user_id = self.sp.me()['id']

        self.playlist_name = "Now Playing History"
        self.playlist_tracks = []

    def init_conn(self, username):
        scope = "playlist-modify-public"
        token = util.prompt_for_user_token(username,scope,redirect_uri='http://localhost')
        
        if token:
            return spotipy.Spotify(auth=token)
        else: 
            print "Can't get token for ", username
            sys.exit(1)

    def check_playlist_exists(self):
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == self.playlist_name:
                self.playlist_id = playlist['id']
                for track in self.sp.user_playlist_tracks(self.user_id, self.playlist_id)['items']:
                    self.playlist_tracks.append(track['track']['uri'])
                return
                
        self.playlist_id = self.sp.user_playlist_create(self.user_id, self.playlist_name)['id']

       

    def search(self, query):
        # Restrict results to 1
        print query
        results = self.sp.search(query, type="track", limit = 1)
        
        for track in results['tracks']['items']:
            return track['id']

        return None
        
    def add_tracks_to_playlist(self, tracks):
        self.sp.user_playlist_add_tracks(self.user_id, self.playlist_id, tracks)
        

class NowPlayingHistory:
    def __init__(self, history_file):
        with open(history_file) as f:
            self.track_history = json.load(f)

if len(sys.argv) > 2:
    username = sys.argv[1]
    history_file = sys.argv[2]
else:
    print "Usage: %s username history_file" % (sys.argv[0],)
    sys.exit()

sp = SpotifyConn(username)
sp.check_playlist_exists()

#nph = NowPlayingHistory()
nph = {}
nph = NowPlayingHistory(history_file)

tracks = []

# Collect all tracks
for track in nph.track_history:
    try:
        track_id = sp.search(track['artist'] + " " + track['title'])
    except:
        pass
    if track_id:
        track_uri = "spotify:track:" + track_id 
        # Filter all duplicates
        if track_uri not in tracks and track_uri not in sp.playlist_tracks:
            tracks.append("spotify:track:" + track_id) 


# Add 25 tracks at once to prevent 413s
batches = []
counter = 0 
batches.append([])

for index, track in enumerate(tracks):
    if index != 0 and index % 25 == 0:
        counter = counter + 1
        batches.append([])

    batches[counter].append(track) 

for batch in batches:
    if batch:
        sp.add_tracks_to_playlist(batch)
    
        
