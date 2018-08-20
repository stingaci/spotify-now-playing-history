# spotify-now-playing-history

This is a simple script that will go through the history captured by the [Now Playing List App](https://play.google.com/store/apps/details?id=com.imihov.nowplaying_list) and create a Now Playing History playlist on Spotify with the respective songs. 

In order to use this tool follow these steps:

1. Open the Now Playing List app, open the hamburger menu in the top right, click on export, and choose JSON 
2. Bring this JSON file wherever you're planing to use this script 
3. Run this tool as follows. You will need to run this somewhere with browser access :
```
Usage: python syncer.py username history_file
```
4. You will need to authorize the use of this app with Spotify by loggining in and then providing the returned URL after authorizing back to the app as requested

Other notes: 

* You will need a Client ID and Client Secret from Spotify. Use Env vars to supply them
* This app takes care of duplicates and ensure no duplicates (ie. same track ID) will ever exist in the playlists  

