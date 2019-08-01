import spotipy
import spotipy.util as util

import os
import csv
import math

import ClassifierBuilder

import pandas as pd
from sklearn.externals import joblib

# Keys to get from System Variables that allow access to Spotify API
client_id = os.environ.get('SPOTIFY_CLIENT_ID_KEY')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET_KEY')
redirect = os.environ.get('SPOTIFY_REDIRECT_URL')

# Scope for personal token usage
scope = 'user-library-read'


# Interacts with Spotify API and gets data for all the songs in 4
# playlists where each playlist represents Rap, Pop, Rock, and Country
# Writes all the data to a CSV
def print_songs(spotify_personal, username):

    print("Interacting with Spotify API\n")

    # Spotify Playlist URLs
    list_playlists = ["spotify:playlist:6aUVcyyhGJ6LZfXNYgDbC7",  # Rap
                      "spotify:playlist:4eFNbpDSEgJ7imq5IHJUou",  # Pop
                      "spotify:playlist:5ewNXA6SGPxTunHkmAVlFU",  # Country
                      "spotify:playlist:6eaaPlF4jIgG2YJt2f5IYC"]  # Metal

    list_rating = [1,   # Rap
                   0,   # Pop
                   -1,  # Country
                   -2]  # Metal

    # CSV File writer
    csv_file = open('data.csv', 'w', newline='', encoding='utf-8')
    spam_writer = csv.writer(csv_file, delimiter=',')

    # Columns in CSV File
    spam_writer.writerow(["Song_Name", "Artist", "Danceability", "Energy", "Key", "Loudness", "Speechiness",
                         "Acousticness", "Instrumentalness", "Liveness", "Valence", "Temp", "Target"])

    # Cycles through the list of playlists and prints the songs.
    for i in range(0, len(list_playlists)):
        # Gets number of songs in playlist
        size = spotify_personal.user_playlist(username, list_playlists[i])["tracks"]["total"]

        # Need to calculate how many times to do offset since only 100 songs' data can be gotten at a time
        num_offsets = math.ceil(size / 100)

        # Loops through playlist with offsets
        for j in range(0, num_offsets):

            # Gets JSON response
            playlists = spotify_personal.user_playlist_tracks(username,
                                                              list_playlists[i],
                                                              offset=(j * 100))

            songs_url = []

            # Extracts all the song URLs from the response to run through another API endpoint
            for k in range(len(playlists['items'])):
                songs_url.append(playlists['items'][k]['track']['external_urls']['spotify'])

            # Gets audio features for all the songs
            audio_features = spotify_personal.audio_features(songs_url)

            # Loops through the audio features for all the songs and writes them to CSV File
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

    # Closes CSV File so it can be used immediately
    csv_file.close()

    print("Done downloading data \n")


# Gets audio features for the song inputted and classifies the genre
def classify_song(spotify_personal, song_url):

    song = [song_url]

    # CSV File writer
    csv_file = open('single_song.csv', 'w', newline='', encoding='utf-8')
    spam_writer = csv.writer(csv_file, delimiter=',')

    # Columns in CSV File
    spam_writer.writerow(["Song_Name", "Artist", "Danceability", "Energy", "Key", "Loudness", "Speechiness",
                          "Acousticness", "Instrumentalness", "Liveness", "Valence", "Temp", "Target"])

    # Gets audio features for the song and the name of the song
    audio_features = spotify_personal.audio_features(song)
    track = spotify_personal.track(song[0])

    # Writes the audio characteristics of the songs to CSV
    spam_writer.writerow([track['name'],
                          track['album']['artists'][0]['name'],
                          audio_features[0]["danceability"],
                          audio_features[0]["energy"],
                          audio_features[0]["key"],
                          audio_features[0]["loudness"],
                          audio_features[0]["speechiness"],
                          audio_features[0]["acousticness"],
                          audio_features[0]["instrumentalness"],
                          audio_features[0]["liveness"],
                          audio_features[0]["valence"],
                          audio_features[0]["tempo"]])

    # Closes CSV File so it can be used immediately
    csv_file.close()

    # Gets machine learning model from file system
    classifier = joblib.load('classifier.sav')

    # Reads the data of the song
    song_data = pd.read_csv("single_song.csv")
    song_splice = song_data[["Danceability", "Energy", "Loudness",
                             "Speechiness", "Acousticness", "Instrumentalness",
                             "Liveness", "Valence"]].values

    # Using the model classifies the genre of the song
    prediction = classifier.predict_proba(song_splice)

    # Prints prediction
    print(classifier.predict(song_splice))

    # Prints the probabilities of all the prediction
    print(prediction)


# Classifies all the songs in a playlist
def classify_playlist_songs(spotify_personal, username, playlist_url):
    playlist = [playlist_url]

    # CSV File writer
    csv_file = open('playlist_songs.csv', 'w', newline='', encoding='utf-8')
    spam_writer = csv.writer(csv_file, delimiter=',')

    # Columns in CSV File
    spam_writer.writerow(["Song_Name", "Artist", "Danceability", "Energy", "Key", "Loudness", "Speechiness",
                          "Acousticness", "Instrumentalness", "Liveness", "Valence", "Temp", "Target"])

    # Gets number of songs in playlist
    size = spotify_personal.user_playlist(username, playlist[0])["tracks"]["total"]

    # Need to calculate how many times to do offset since only 100 songs' data can be gotten at a time
    num_offsets = math.ceil(size / 100)

    # Loops through playlist with offsets
    for j in range(0, num_offsets):

        # Gets JSON response
        playlists = spotify_personal.user_playlist_tracks(username,
                                                          playlist[0],
                                                          offset=(j * 100))

        songs_url = []

        # Extracts all the song URLs from the response to run through another API endpoint
        for k in range(len(playlists['items'])):
            songs_url.append(playlists['items'][k]['track']['external_urls']['spotify'])

        # Gets audio features for all the songs
        audio_features = spotify_personal.audio_features(songs_url)

        # Loops through the audio features for all the songs and writes them to CSV File
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
                                  audio_features[k]["tempo"]])

    # Closes CSV File so it can be used immediately
    csv_file.close()

    # Gets machine learning model from file system
    classifier = joblib.load('classifier.sav')

    # Reads the data of the songs
    song_data = pd.read_csv("playlist_songs.csv")
    song_splice = song_data[["Danceability", "Energy", "Loudness",
                             "Speechiness", "Acousticness", "Instrumentalness",
                             "Liveness", "Valence"]].values

    # Using the model classifies the genre of the songs
    prediction = classifier.predict_proba(song_splice)

    # print(classifier.predict(song_splice))

    # Prints prediction
    print(prediction)


def main():

    user = ""

    # Used to store a username in a text file and access it
    try:
        file = open('user.txt')

        if file.mode == 'r':
            user = file.read()

        file.close()

    # Handles error where there is no username saved
    except FileNotFoundError:
        print("We need your username to proceed: ")
        user = input()

        file = open("user.txt", "w+")

        if file.mode == 'w+':
            file.write("" + user)

        file.close()

    # Used to access user data
    personal_token = util.prompt_for_user_token(user,
                                                scope,
                                                client_id,
                                                client_secret,
                                                redirect)

    # API Wrapper objects to use functions to interact with Spotify API
    spotify_personal = spotipy.Spotify(personal_token)

    # Username of person logged in
    username = spotify_personal.current_user()["id"]

    exit_var = False

    # Loop for interface
    while not exit_var:
        print("Choose an option")
        print("1 - Analyze a playlist")
        print("2 - Analyze a song")
        print("3 - Retrain")
        print("4 - Exit")

        choice = input("Choice: ")

        # Allows user to input a playlist and get back predictions
        if choice == "1":
            playlist_url = input("Playlist URL: ")

            classify_playlist_songs(spotify_personal, username, playlist_url)

            print()

        # Allows user to input a song and get back a prediction
        elif choice == "2":
            song_url = input("Song URL: ")

            classify_song(spotify_personal, song_url)

            print()

        # Retrains model
        elif choice == "3":
            print("Training (Might take a few minutes)\n")

            print_songs(spotify_personal, username)

            ClassifierBuilder.build_classifier()

            print("Finished Training\n")

        # Exit
        elif choice == "4":
            exit_var = True

        # Handles any invalid input
        else:
            print("Invalid Input.\n")


# Program entrance
if __name__ == "__main__":
    main()
