from Preferences import Preferences
from API import API

preferences = Preferences()
preferences.load_from_env()

spotify_api = API(preferences)
