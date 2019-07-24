import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
import os

client_id = os.environ.get('SPOTIFY_CLIENT_ID_KEY')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET_KEY')
username = "1267918568" # My Personal Spotify User Name
redirect = os.environ.get('SPOTIFY_REDIRECT_URL')
scope = 'user-library-read'

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))


credentials = oauth2.SpotifyClientCredentials(client_id,
                                              client_secret)

personalToken = util.prompt_for_user_token(username,
                                                 scope,
                                                 client_id,
                                                 client_secret,
                                                 redirect)

oauthtoken = credentials.get_access_token()

spotifyOauth = spotipy.Spotify(oauthtoken)
spotifyPersonal = spotipy.Spotify(personalToken)

if (spotifyPersonal):
    playlists = spotifyPersonal.user_playlists(username)

    print(playlists)

    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print
            print(playlist['name'])
            print('  total tracks', playlist['tracks']['total'])
            results = spotifyPersonal.user_playlist(username, playlist['id'],
                                       fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks)
            while tracks['next']:
                tracks = spotifyPersonal.next(tracks)
                show_tracks(tracks)
else:
    print("Can't get token for", username)

print()

if oauthtoken:
    results = spotifyOauth.audio_analysis("spotify:track:1oJbzZINptfVVsi8SYWFqW")
    results2 = spotifyOauth.audio_features(tracks=["spotify:track:1oJbzZINptfVVsi8SYWFqW"])

    print(results)
    print(results2)
else:
    print("Can't get token for", username)