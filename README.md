# Spotify Genre Classifier
## Overview
This program helps users classify songs into 4 genres (Rap, Pop, Country, Metal) to help users determine whether a song is more aligned with their tastes and to help guide their music listening. Currently the genres are aligned to what I like/do not like. It uses Scikit Learn along with the Spotify API to pull audio features data from songs from 4 playlists (rap, pop, country, metal) to build a machine learning model to classify songs into a genre. It performs parameter tuning on a variety of classification models to find the best hyperparameters. Once all the best hyperparameters are found, it performs cross validation amongst the classifiers and their best parameters to find the top classification method by looking at mean accuracy. Once a model has been detected, trained, and saved to disk, the program allows the user to enter a spotify song url to classify that one song or a playlist url to classify all the songs in the playlist.

Most of the error in classifications happens when a song can pass as a song in both genres for example rap/pop. To combat this, classification probabilities are shown to make it more transparent. To find the features which were helpful for classifications, the method done so is detailed in the data_science folder (WIP). The data_science folder contains a Jupyter notebook file where I did data science work to explore how audio features differ for songs of different genres and what audio features are most helpful for classification.

## Technical Features
* Python used to do the whole project
* Scikit Learn used to perform machine learning on the data set and to build models
* Pandas/Numpy provides powerful data structures used through out the program
* Spotify API to gather data for model buiilding and for classification

## Set Up
Dependencies needed: 
```
Spotipy
Scikit Learn
Pandas
Numpy
 ```
All of these are available to be downloaded through pip
 
### Running
Using this program requires `client_id` and `client_secret` keys from Spotify.

This can be gotten from `https://developer.spotify.com/dashboard/`

Log in and create an app on the website.

Once created, Spotify will serve you with `client_id` and `client_secret` keys.

<-- More steps for using program successfully will be included here in the near future-->

Navigate to `src` folder and run `python main.py`

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
