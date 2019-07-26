import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
import os
import csv

client_id = os.environ.get('SPOTIFY_CLIENT_ID_KEY')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET_KEY')
username = "1267918568" # My Personal Spotify User Name
redirect = os.environ.get('SPOTIFY_REDIRECT_URL')
scope = 'user-library-read'


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
    playlists = spotifyPersonal.user_playlist_tracks(username, 'spotify:playlist:1lF6y6T2DtEsExx04J3i3z')

    with open('test.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')

        spamwriter.writerow(["Song_Name", "Artist", "Danceability", "Energy", "Key", "Loudness", "Speechiness",
                             "Acousticness", "Instrumentalness", "Liveness", "Valence", "Temp", "Target"])

        songsURL = []

        for i in range(len(playlists['items'])):
            songsURL.append(playlists['items'][i]['track']['external_urls']['spotify'])

        audioFeatures = spotifyPersonal.audio_features(songsURL)

        # print(audioFeatures)

        for i in range(len(playlists['items'])):
            song = playlists['items'][i]

            spamwriter.writerow([(song)['track']['name'], (song)['track']['album']['artists'][0]['name'],
                                 audioFeatures[i]["danceability"], audioFeatures[i]["energy"], audioFeatures[i]["key"],
                                 audioFeatures[i]["loudness"], audioFeatures[i]["speechiness"],
                                 audioFeatures[i]["acousticness"],
                                 audioFeatures[i]["instrumentalness"], audioFeatures[i]["liveness"],
                                 audioFeatures[i]["valence"],
                                 audioFeatures[i]["tempo"], 0])

# -------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------------

    playlists = spotifyPersonal.user_playlist_tracks(username, 'spotify:playlist:6jMFho3Kra6mALORsAk5t0')

    with open('test.csv', 'a', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')

        songsURL = []

        for i in range(len(playlists['items'])):
            songsURL.append(playlists['items'][i]['track']['external_urls']['spotify'])

        audioFeatures = spotifyPersonal.audio_features(songsURL)

        #print(audioFeatures)


        for i in range(len(playlists['items'])):
            song = playlists['items'][i]

            spamwriter.writerow([(song)['track']['name'], (song)['track']['album']['artists'][0]['name'], audioFeatures[i]["danceability"],audioFeatures[i]["energy"],audioFeatures[i]["key"],
                                                 audioFeatures[i]["loudness"],audioFeatures[i]["speechiness"],audioFeatures[i]["acousticness"],
                                                 audioFeatures[i]["instrumentalness"],audioFeatures[i]["liveness"],audioFeatures[i]["valence"],
                                                 audioFeatures[i]["tempo"],0])


        #-------------------

        playlists = spotifyPersonal.user_playlist_tracks(username, 'spotify:playlist:6jMFho3Kra6mALORsAk5t0', offset=100)

        with open('test.csv', 'a', newline='', encoding='utf-8') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')

            songsURL = []

            for i in range(len(playlists['items'])):
                songsURL.append(playlists['items'][i]['track']['external_urls']['spotify'])

            audioFeatures = spotifyPersonal.audio_features(songsURL)

            # print(audioFeatures)

            for i in range(len(playlists['items'])):
                song = playlists['items'][i]

                spamwriter.writerow([(song)['track']['name'], (song)['track']['album']['artists'][0]['name'],
                                     audioFeatures[i]["danceability"], audioFeatures[i]["energy"],
                                     audioFeatures[i]["key"],
                                     audioFeatures[i]["loudness"], audioFeatures[i]["speechiness"],
                                     audioFeatures[i]["acousticness"],
                                     audioFeatures[i]["instrumentalness"], audioFeatures[i]["liveness"],
                                     audioFeatures[i]["valence"],
                                     audioFeatures[i]["tempo"], 0])

    # -------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------------

    playlists = spotifyPersonal.user_playlist_tracks(username, 'spotify:playlist:3pvmGEC1CbUF5QNfycVXjA')

    with open('test.csv', 'a', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')

        songsURL = []

        for i in range(len(playlists['items'])):
            songsURL.append(playlists['items'][i]['track']['external_urls']['spotify'])

        audioFeatures = spotifyPersonal.audio_features(songsURL)

        #print(audioFeatures)

        for i in range(len(playlists['items'])):
            song = playlists['items'][i]

            spamwriter.writerow([(song)['track']['name'], (song)['track']['album']['artists'][0]['name'], audioFeatures[i]["danceability"],audioFeatures[i]["energy"],audioFeatures[i]["key"],
                                                 audioFeatures[i]["loudness"],audioFeatures[i]["speechiness"],audioFeatures[i]["acousticness"],
                                                 audioFeatures[i]["instrumentalness"],audioFeatures[i]["liveness"],audioFeatures[i]["valence"],
                                                 audioFeatures[i]["tempo"],0])




    playlists = spotifyPersonal.user_playlist_tracks(username, 'spotify:playlist:3pvmGEC1CbUF5QNfycVXjA', offset=100)

    with open('test.csv', 'a', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')

        songsURL = []

        for i in range(len(playlists['items'])):
            songsURL.append(playlists['items'][i]['track']['external_urls']['spotify'])

        audioFeatures = spotifyPersonal.audio_features(songsURL)

        # print(audioFeatures)

        for i in range(len(playlists['items'])):
            song = playlists['items'][i]

            spamwriter.writerow([(song)['track']['name'], (song)['track']['album']['artists'][0]['name'],
                                 audioFeatures[i]["danceability"], audioFeatures[i]["energy"], audioFeatures[i]["key"],
                                 audioFeatures[i]["loudness"], audioFeatures[i]["speechiness"],
                                 audioFeatures[i]["acousticness"],
                                 audioFeatures[i]["instrumentalness"], audioFeatures[i]["liveness"],
                                 audioFeatures[i]["valence"],
                                 audioFeatures[i]["tempo"], 0])
#-------------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------------

    playlists = spotifyPersonal.user_playlist_tracks(username, 'spotify:playlist:6vpLNtSBeiHzB3JODqjg79')

    with open('test.csv', 'a', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')

        songsURL = []

        for i in range(len(playlists['items'])):
            songsURL.append(playlists['items'][i]['track']['external_urls']['spotify'])

        audioFeatures = spotifyPersonal.audio_features(songsURL)

        #print(audioFeatures)

        for i in range(len(playlists['items'])):
            song = playlists['items'][i]

            spamwriter.writerow([(song)['track']['name'], (song)['track']['album']['artists'][0]['name'], audioFeatures[i]["danceability"],audioFeatures[i]["energy"],audioFeatures[i]["key"],
                                                 audioFeatures[i]["loudness"],audioFeatures[i]["speechiness"],audioFeatures[i]["acousticness"],
                                                 audioFeatures[i]["instrumentalness"],audioFeatures[i]["liveness"],audioFeatures[i]["valence"],
                                                 audioFeatures[i]["tempo"], 0])

print()
