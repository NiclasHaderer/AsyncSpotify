# Examples

## Getting started

If you want to start connecting to the spotify api you have to create a new instance of the `Preferences`. These Preferences hold all sorts of configurations.  

```python
from async_spotify import Preferences

preferences = Preferences(
    application_id = 'Your id',
    application_secret = 'Your secret',
    scopes = ['your', 'scopes'],
    redirect_url = 'your.redirect.utl')

# You can also load the preferences from environment variables.  
# If the variable does not exist the existing value will not be overwritten.
preferences.load_from_env()
```

These created preferences have to be passed to the `SpotifyApiClient`.  

```python
# Create new client
api_client = SpotifyApiClient(prefernces)
```

To get a code from Spotify the user has to agee to the scopes your app asks for.  
For this you create an authorization, let the user visit this url and read the code parameter in the spotify redirect.  
If you have some questions about this process read [this](https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow) spotify aritcle about it.

```python
# Build the authorization url for the users

authorization_url: str = api_client.build_authorization_url(show_dialog = True)
```

We will assue that you managed to get a code from spotify for a specific user.  

Now we have to excange the code for an authorization token and a refresh token. But before we make this we have to create a new client which will be internally used for all the request making.

```python
# Create a new client which will handle the request
await api_client.create_new_client()

# Exchange the code for the tokens
auth_token: SpotifyAuthorisationToken = await api.get_auth_token_with_code(code)
```

After we recieved the `auth_token` we can start making request.  

```python
# Get information about an album
album = await api_client.albums.get_one(album_id, market='DE', auth_token=auth_token)
# ...
```

If you want to shut down your application and don't want to leak requests you have to call the `close_client` method of the `api_client`.

```python
# Close the client
await api_client.close_client()
```

## Endpoints

Every Api Endpoint is represented as an instance variables of the `SpotifyApiClient`.  
Look [here](https://huiibuh.github.io/AsyncSpotify/public_api/spotify_api_client/) for every instance variable and the associated classes.  

```python
# For the albums endpoint
api_client.albums.whatever()
# For the artist endpoint
api_client.artist.whatever()
```

## Advanced Configuration

If you don't want to pass the `auth_token` every time you make a request you can instruct the `SpotifyApiClient` to keep the token in memmory. Every time you refresh the token the in memmory token will be updated too. So you always have a valid token you can make requests with. If the token expires you will still have to refresh it yourself by calling the `refresh_token` method, which will returned the updated token. You dont have to pass a token to the method however if you want the internal token to be updated.  
In addition to that you can limit the simulatnious requests and the timout if you create a new client.

```python
api_client = SpotifyApiClient(preferences, hold_authentication=True)

# And if you already have a auth_token you can pass this token to the constructor
api_client = SpotifyApiClient(preferences, hold_authentication=True, auth_token=auth_token)
# Make the requests without passing the auth_token every time
album = await api_client.albums.get_one(album_id)

# Limit the requests and the timeout
await api_client.create_new_client(request_limit=1500, request_timeout=30)

```

## Exceptions

There are multiple exception which could get raised by the `SpotifyApiClient`.  
Every exception inherits from the `SpotifyBaseError` so if you want to catch every spotify exception you can do it with the `SpotifyBaseError`.  

+ The `SpotifyError` exception gets raised for general usage errors
+ The `TokenExpired` exception gets raised if the spotify token used for making an api call is expired
+ The `RateLimitExceeded` exception gets raised if the raite limit is exceeded
+ The `SpotifyAPIError` exception gets raised for general errors like a invalid album id

Each of the exceptions implements the `get_json()` method which will return the follwing json:

```json
{
    error: {
        status: 0,
        message: ''
    }
}
```

The status is the HTTP status code and if not aplicable the number 0.
The message is the reason something failed.  

```python
try:
    album = await api_client.albums.get_one(album_id)
except SpotifyAPIError as error:
    error = error.get_json()
    # Do something with the error message
```

## Code retrieval with a cookie

Normally you have to get the code with the client credential workflow. If your user has already agreed to the scopes and you have the cookie of the user you can get rid of this process.  
This is mostely intended for testing purposes, but you could also use it in your production environment in the very unlikely edge case that you have the spotify cookie of your user.  

You start like normal and create a new `SpotifyApiClient`.

```python
preferences = Preferences()
preferences.load_from_env()

api_client = SpotifyApiClient(preferences, hold_authentication=True)

# Create a new spotify cookie
cookie = SpotifyCookie()
# Load the cookie from a file (you can also use the constructor to pass the data)
cookies.load_from_file('Path/to/cookie.json')

# Get the coke with the spotify cookie
code = await api.get_code_with_cookie(cookie)

# Use the retrieved code to get the auth token
auth_token = await api.get_auth_token_with_code(code)

album = await api_client.albums.get_one(album_id)

await api_client.close_client()
```

Format of the *cookie.json*

```json
{
    "sp_t"  : "a",
    "sp_dc" : "b",
    "sp_key": "c"
}
```
