import spotipy
import spotipy.oauth2 as oauth2
import spotipy.util as util
import os
import csv
import math
from .ClassifierBuilder import ClassifierBuilder

import matplotlib as mpl

client_id = os.environ.get('SPOTIFY_CLIENT_ID_KEY')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET_KEY')
redirect = os.environ.get('SPOTIFY_REDIRECT_URL')
scope = 'user-library-read'


def print_songs(spotify_personal, username):

    list_playlists = ["spotify:playlist:6aUVcyyhGJ6LZfXNYgDbC7",  # Rap
                      "spotify:playlist:4eFNbpDSEgJ7imq5IHJUou",  # Pop
                      "spotify:playlist:5ewNXA6SGPxTunHkmAVlFU",  # Country
                      "spotify:playlist:6eaaPlF4jIgG2YJt2f5IYC"]  # Metal

    list_rating = [1, 0, -1, -2]

    with open('data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spam_writer = csv.writer(csvfile, delimiter=',')

        spam_writer.writerow(["Song_Name", "Artist", "Danceability", "Energy", "Key", "Loudness", "Speechiness",
                             "Acousticness", "Instrumentalness", "Liveness", "Valence", "Temp", "Target"])

    for i in range(0, len(list_playlists)):
        size = spotify_personal.user_playlist(username, list_playlists[i])["tracks"]["total"]

        num_offsets = math.ceil(size / 100)

        for j in range(0, num_offsets):

            playlists = spotify_personal.user_playlist_tracks(username,
                                                              list_playlists[i],
                                                              offset=(j * 100))

            with open('data.csv', 'a', newline='', encoding='utf-8') as csvfile:
                spam_writer = csv.writer(csvfile, delimiter=',')

                songs_url = []

                for k in range(len(playlists['items'])):
                    songs_url.append(playlists['items'][k]['track']['external_urls']['spotify'])

                audio_features = spotify_personal.audio_features(songs_url)

                for k in range(len(playlists['items'])):
                    song = playlists['items'][k]

                    spam_writer.writerow([song['track']['name'],
                                         song['track']['album']['artists'][0]['name'],
                                         audio_features[k]["danceability"],
                                         audio_features[k]["energy"],
                                         audio_features[k]["key"],
                                         audio_features[k]["loudness"],
                                         audio_features[k]["speechiness"],
                                         audio_features[k]["acousticness"],
                                         audio_features[k]["instrumentalness"],
                                         audio_features[k]["liveness"],
                                         audio_features[k]["valence"],
                                         audio_features[k]["tempo"],
                                         list_rating[i]])


def main():

    print(mpl.get_configdir)

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

    personal_token = util.prompt_for_user_token(user,
                                                scope,
                                                client_id,
                                                client_secret,
                                                redirect)

    oauth_token = credentials.get_access_token()

    spotify_oauth = spotipy.Spotify(oauth_token)
    spotify_personal = spotipy.Spotify(personal_token)

    username = spotify_personal.current_user()["id"]

    exit = False

    while exit == False:
        print("Choose an option")
        print("1 - Analyze a playlist")
        print("2 - Analyze a song")
        print("3 - Retrain")
        print("4 - Exit")

        choice = input("Choice: ")

        if choice == "1":
            print()

        elif choice == "2":
            print()

        elif choice == "3":
            print("Training (Might take a few minutes)\n")
            ClassifierBuilder.build_classifier()
            print("Finished Training\n")

        elif choice == "4":
            exit = True

        else:
            print("Invalid Input.\n")


if __name__ == "__main__":
    main()
