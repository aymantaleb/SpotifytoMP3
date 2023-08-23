# SpoitfytoMP3

## Created by Ayman Taleb 08/21/2023

A python script to take a Spotify playlist using [Spotipy](https://spotipy.readthedocs.io/en/master/#), scape Youtube for the songs using [pytube](https://pytube.io/en/latest/index.html), and run the URLs through [Youtube-dl](https://github.com/ytdl-org/youtube-dl).

As of now it only goes through the playlists and returns a list of the urls and video titles. Planning on writing the data to a CSV and automatically downloading the videos. 

---

### Issue with pytube search function
I have noticed there is an issue with the pytube search function regarding certain video renderers. I fixed this by modifying the search class:
In the ['fetch_and_parse'](#code) item_renderer conditional for loop I added ['
                if 'reelShelfRenderer' in video_details:
                    continue

                if 'showingResultsForRenderer' in video_details:
                    continue
                
                if 'movieRenderer' in video_details:
                    continue
'](#code) Which seemed to fix the errors I was getting