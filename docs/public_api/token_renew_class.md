If you want to add a hook to update the Api token automatically you can do this by passing your own class to the [SpotifyApiClient](spotify_api_client.md).  

Your class has to extend the `TokenRenewClass` and provide an `async __call__()` method which returns the new [Auth Token](authentification.md). 

::: async_spotify.token_renew_class
