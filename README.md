# SpoitfytoMP3

## Created by Ayman Taleb 08/21/2023

A multi-threaded python script to take a Spotify playlist using [spotipy](https://spotipy.readthedocs.io/en/master/#), downloads the songs from Youtube using [pytube](https://pytube.io/en/latest/index.html) in mp4 format, and using [FFmpeg](https://ffmpeg.org/download.html) to convert the mp4s from Youtube to mp3 files. I created this to add music to a game (Fallout: New Vegas), which requires the audio to be in mp3 format. Using [Extended New Vegas Radio Generator](https://www.nexusmods.com/newvegas/mods/36835) to add the songs to the in-game radio. 

It works by taking your playlist URL and compiles a list of the songs and artists, then it donwloads the album art associated with the song (this is for a GUI I want to eventually make), then it finds Youtube videos of the songs, then it downloads the video as an mp4 since pytube is only capable of that, and finally it uses FFmpeg to convert the mp4s to mp3s. If an album art is not found it will just use the oldmanShrug.jpg instead. 

You will need to generate a Spotify client_id, client_sercretand URI to access the [Spotify API](https://developer.spotify.com/documentation/web-api). And for each playlist you want to pull, you need the playlist id, which can be [found in the URL](https://clients.caster.fm/knowledgebase/110/How-to-find-Spotify-playlist-ID.html).

---

### Issue with pytube search function
I have noticed there is an issue with the pytube search function regarding certain video renderers. I fixed this by modifying the search class:
In the fetch_and_parse item_renderer conditional's for loop I added 

               if 'reelShelfRenderer' in video_details:
                    continue

                if 'showingResultsForRenderer' in video_details:
                    continue
                
                if 'movieRenderer' in video_details:
                    continue' 
Which seemed to fix the errors I was getting