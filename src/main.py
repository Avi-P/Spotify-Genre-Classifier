import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
import os
import csv
import math

client_id = os.environ.get('SPOTIFY_CLIENT_ID_KEY')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET_KEY')
redirect = os.environ.get('SPOTIFY_REDIRECT_URL')
scope = 'user-library-read'


def print_songs(listPlaylists, listRating, spotifyPersonal, username):
    with open('test.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')

        spamwriter.writerow(["Song_Name", "Artist", "Danceability", "Energy", "Key", "Loudness", "Speechiness",
                             "Acousticness", "Instrumentalness", "Liveness", "Valence", "Temp", "Target"])

    for i in range(0, len(listPlaylists)):
        size = spotifyPersonal.user_playlist(username, listPlaylists[i])["tracks"]["total"]

        num_offsets = math.ceil(size / 100)

        for j in range(0, num_offsets):

            playlists = spotifyPersonal.user_playlist_tracks(username,
                                                             listPlaylists[i],
                                                             offset=(j * 100))

            with open('test.csv', 'a', newline='', encoding='utf-8') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',')

                songsURL = []

                for k in range(len(playlists['items'])):
                    songsURL.append(playlists['items'][k]['track']['external_urls']['spotify'])

                audioFeatures = spotifyPersonal.audio_features(songsURL)

                for k in range(len(playlists['items'])):
                    song = playlists['items'][k]

                    spamwriter.writerow([song['track']['name'],
                                         song['track']['album']['artists'][0]['name'],
                                         audioFeatures[k]["danceability"],
                                         audioFeatures[k]["energy"],
                                         audioFeatures[k]["key"],
                                         audioFeatures[k]["loudness"],
                                         audioFeatures[k]["speechiness"],
                                         audioFeatures[k]["acousticness"],
                                         audioFeatures[k]["instrumentalness"],
                                         audioFeatures[k]["liveness"],
                                         audioFeatures[k]["valence"],
                                         audioFeatures[k]["tempo"],
                                         listRating[i]])


def main():

    user = ""

    try:
        file = open('user.txt')

        if file.mode == 'r':
            user = file.read()

        file.close()

    except FileNotFoundError:
        print("We need your username to proceed: ")
        user = input()

        file = open("user.txt", "w+")

        if file.mode == 'w+':
            file.write("" + user)

        file.close()

    credentials = oauth2.SpotifyClientCredentials(client_id,
                                                  client_secret)

    personalToken = util.prompt_for_user_token(user,
                                               scope,
                                               client_id,
                                               client_secret,
                                               redirect)

    oauthtoken = credentials.get_access_token()

    spotifyOauth = spotipy.Spotify(oauthtoken)
    spotifyPersonal = spotipy.Spotify(personalToken)

    username = spotifyPersonal.current_user()["id"]

    listPlaylists = ["spotify:playlist:6aUVcyyhGJ6LZfXNYgDbC7",  # Rap
                     "spotify:playlist:4eFNbpDSEgJ7imq5IHJUou",  # Pop
                     "spotify:playlist:5ewNXA6SGPxTunHkmAVlFU",  # Country
                     "spotify:playlist:6eaaPlF4jIgG2YJt2f5IYC"]  # Metal

    listRating = [1, 0, -1, -2]

    print_songs(listPlaylists, listRating, spotifyPersonal, username)


if __name__ == "__main__":
    main()