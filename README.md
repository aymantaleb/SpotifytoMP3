# SpotifytoMP3

## Created by Ayman Taleb 08/21/2023

A multi-threaded python script to take a Spotify playlist using [spotipy](https://spotipy.readthedocs.io/en/master/#), downloads the songs from Youtube using [pytube](https://pytube.io/en/latest/index.html) in mp4 format, and using [FFmpeg](https://ffmpeg.org/download.html) to convert the mp4s from Youtube to mp3 files. I created this to add music to a game (Fallout: New Vegas), which requires the audio to be in mp3 format. Using [Extended New Vegas Radio Generator](https://www.nexusmods.com/newvegas/mods/36835) to add the songs to the in-game radio. 

It works by taking your playlist URL and compiles a list of the songs and artists, then it donwloads the album art associated with the song (this is for a GUI I want to eventually make), then it finds Youtube videos of the songs, then it downloads the video as an mp4 since pytube is only capable of that, and finally it uses FFmpeg to convert the mp4s to mp3s. If an album art is not found it will just use the oldmanShrug.jpg instead. 

You will need to generate a Spotify client_id, client_sercret and URI to access the [Spotify API](https://developer.spotify.com/documentation/web-api). For now this will not work unless you create your own Spotify extension and use those ids to run this script. I will work on making this available for anyone to use just with a Spotify log in if need be. And for each playlist you want to pull, you need the playlist link. So that you won't have to hardcode the client_id and client_secret, you can just add them to your environment variables:

Windows:
<ol>
<li>Open the Start menu and search for "Environment Variables."

<li>Click on "Edit the system environment variables."

<li>In the "System Properties" window, click the "Environment Variables" button.

<li>Under the "User variables" section, click "New" to add a new environment variable.

<li>Enter SPOTIPY_CLIENT_ID for the "Variable name" and your actual Spotify client ID for the "Variable value." Repeat this step for SPOTIPY_CLIENT_SECRET and SPOTIPY_REDIRECT_URI as well.

<li>Click "OK" to close each of the windows.

</ol>

macOS or Linux:
You can set environment variables directly in your terminal session or by adding them to your shell's configuration file (e.g., .bashrc, .zshrc, or similar) to make them persist across sessions.

For example, in your terminal, you can set environment variables like this:

                export SPOTIPY_CLIENT_ID='your-spotify-client-id'
                export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
                export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

Or add them to the shell's configuration file:

                source ~/.bashrc  # or source ~/.zshrc if using Zsh

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
Which seemed to fix the errors I was getting. I got this idea from this [issue posted on the pytube Github.](https://github.com/pytube/pytube/issues/1270#issuecomment-1436041377)
