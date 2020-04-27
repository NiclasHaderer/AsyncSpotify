# Overview

In here are all the different endpoints which are necessary for accessing the spotify api.
Each of the endpoints can only be accessed through the [SpotifyApiClient](../spotify_api_client.md).
Every endpoint is an instance variable of the [SpotifyApiClient](../spotify_api_client.md).
You should only interact through this way with the Endpoints.
The Endpoint instance name is the name of the class in lower case. 

## Example

```python

# To access the Albums endpoint use
spotify_api_client.albums.whatever_method()

# To access the Artist endpoint use
spotify_api_client.artist.whatever_method()
```

## Available Endpoints:

+ [Album](albums.md)
+ [Artist](artists.md)
+ [Browse](browse.md)
+ [Episodes](episodes.md)
+ [Follow](follow.md)
+ [Library](library.md)
+ [Personalization](personalization.md)
+ [Player](player.md)
+ [Playlist](playlists.md)
+ [Search](search.md)
+ [Shows](shows.md)
+ [Tracks](tracks.md)
+ [User](user.md)
