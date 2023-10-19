import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import threading
import time
import pytube as pyt
from PIL import Image
from urllib.request import urlopen
import os
import shutil
import re
import subprocess

#gets the album art through Spotify
#was thinking of making a GUI or webpage for this so pulling the album art would be used for that
def getAlbumArt(tracks):
    artPath = "./AlbumArt/"

    for item in tracks:
        track = item["track"]
        trackName = track["name"]
        trackName = re.sub(r'[\\/:"*?<>|]+', "", trackName)
        if track["album"]["images"]:
            albumArtURL = track["album"]["images"][0]["url"]
            img = Image.open(urlopen(albumArtURL))
            img.save(artPath + trackName + ".jpeg", format="jpeg")
        else:
            print(f"No album art found for track: {track['name']}")
            img = Image.open("oldmanShrug.jpg")
            img.save(artPath + trackName + ".jpeg", format="jpeg")
            continue
    print("\n---art collection done---")



#splits the album art process into num_threads threads, to make it faster
def getAlbumArtThreading(trackList, num_threads):
    chunk_size = len(trackList) // num_threads
    chunks = [
        trackList[i : i + chunk_size] for i in range(0, len(trackList), chunk_size)
    ]

    results = [None] * len(chunks)

    def worker(chunk, results, index):
        results[index] = getAlbumArt(chunk)

    threads = []
    for index, chunk in enumerate(chunks):
        t = threading.Thread(target=worker, args=(chunk, results, index))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()



#gets the track details for each song (name and artist(s))
def getTrackDetails(playlist_id):
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    offset = 0
    tracks = []
    trackDetails = []

    while True:
        playlist = sp.playlist_items(playlist_id, offset=offset, limit=100)
        tracks.extend(playlist["items"])
        if len(playlist["items"]) < 100:
            break
        offset += 100

    #I comment this out to make it run faster, since I do not always need the images
    # getAlbumArtThreading(tracks, 4)
    count = 0

    for item in tracks:
        track = item["track"]
        trackName = track["name"]
        trackName = re.sub(r'[\\/:"*?<>|]+', "", trackName)

        if len(track["artists"]) == 1:
            testString = trackName + "$$" + track["artists"][0]["name"]
            trackDetails.append(testString)
            count += 1
        else:
            artistsComplete = ""
            for i in track["artists"]:
                index = track["artists"].index(i)
                name = track["artists"][index]["name"]
                artistsComplete = artistsComplete + " " + name

            testString = trackName + "$$" + artistsComplete
            trackDetails.append(testString)
            count += 1

    return trackDetails

#takes the names of the songs and gets Youtube URLS
def webScrape(playlist):
    urlList = []

    for i in playlist:
        query = i
        search_results = pyt.Search(query).results

        if search_results:
            video = search_results[0]

            urlList.append(video.watch_url)
        else:
            urlList.append("NOT FOUND")

    return urlList

#threading to make the webscraping faster
def webScrapeThreading(trackList, num_threads):
    chunk_size = len(trackList) // num_threads
    chunks = [
        trackList[i : i + chunk_size] for i in range(0, len(trackList), chunk_size)
    ]

    results = [None] * len(chunks)

    def worker(chunk, results, index):
        results[index] = webScrape(chunk)

    threads = []
    for index, chunk in enumerate(chunks):
        t = threading.Thread(target=worker, args=(chunk, results, index))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return [url for sublist in results for url in sublist]

#to match the art with the songs for the dataframe
def correlate_songs_with_art(songNames, artPath):
    art_dict = {
        os.path.splitext(os.path.basename(artPath))[0]: artPath for artPath in artPath
    }

    correlated = [art_dict.get(song, None) for song in songNames]

    return correlated

#to make a dataframe of the song's names, artist(s), art, and URL
def makeDF(trackList, urlList):
    artPath = [
        os.path.join("./AlbumArt/", fname) for fname in os.listdir("./AlbumArt/")
    ]
    songNames, Artists = zip(*(s.split("$$") for s in trackList))
    art = correlate_songs_with_art(songNames, artPath)
    print(len(songNames), len(Artists), len(urlList), len(art))
    track = {"Songs": songNames, "Artist": Artists, "URL": urlList, "Art Path": art}
    trackDF = pd.DataFrame(track)
    trackDF.to_csv("tracks.csv")
    return trackDF


results_lock = threading.Lock()

#using the URL to download the Youtube video as an audio MP3
def urlToMP3(dataframe, output_path, mp3Results, index):
    try:
        for index, row in dataframe.iterrows():
            video_name = row["Songs"]
            video_url = row["URL"]

            yt = pyt.YouTube(video_url)

            stream = yt.streams.filter(file_extension="mp4").get_highest_resolution()

            print(f"Downloading video '{video_name}'...")

            default_filename = video_name + ".mp4"
            new_filename = video_name + ".mp3"
            stream.download(output_path, filename=default_filename)

            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    os.path.join(output_path, default_filename),
                    os.path.join(output_path, new_filename),
                ]
            )

            print(
                f"Audio file '{video_name}.mp3' downloaded and converted successfully!"
            )
            os.remove(os.path.join(output_path, default_filename))
            with results_lock:
                mp3Results[index] = new_filename

    except Exception as e:
        print("An error occurred:", str(e))

#threading for URLtoMP3
def urlToMP3Threading(dataframe, output_path, num_threads):
    chunk_size = len(dataframe) // num_threads
    chunks = [
        dataframe[i : i + chunk_size] for i in range(0, len(dataframe), chunk_size)
    ]

    mp3Results = [None] * len(dataframe)

    def worker(chunk, mp3Results, index):
        urlToMP3(chunk, output_path, mp3Results, index)

    threads = []
    for index, chunk in enumerate(chunks):
        t = threading.Thread(target=worker, args=(chunk, mp3Results, index))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    playlistURL = input("enter your playlist URL: ")
    playlist_id = playlistURL[playlistURL.index("t/") + 2 : playlistURL.index("?")]
    artPath = "./AlbumArt/"
    if os.path.exists(artPath):
        shutil.rmtree(artPath)

    if not os.path.exists(artPath):
        os.makedirs(artPath)

    audioPath = "./mp3s/"
    if os.path.exists(audioPath):
        shutil.rmtree(audioPath)

    if not os.path.exists(audioPath):
        os.makedirs(audioPath)

    start_time = time.time()
    trackList = getTrackDetails(playlist_id)
    urlList = webScrapeThreading(trackList, 6)
    trackDF = makeDF(trackList, urlList)
    urlToMP3Threading(trackDF, audioPath, 4)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.2f} s")
