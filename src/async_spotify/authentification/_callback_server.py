"""
This file provides a callback server for the spotify auth process. It is intended for automated testing, so use it with
care.
"""

from aiohttp import web
from multidict import MultiDictProxy


async def handle_spotify_callback(request):
    """
    Handle the redirection make by spotify after the oauth dialog
    :return: json
    """
    query_object: MultiDictProxy = request.query
    if "code" in query_object:
        return web.json_response({"code": query_object["code"]})

    return web.json_response({"error": "Could not get the response code from spotify"})


def _create_callback_server(port: int = 1111, callback_route: str = '/test/api/callback'):
    """
    Creates a server for the callback after the oauth dialogue
    :param port: The port the server runs on
    :return: None
    """

    routes: list = [web.get(callback_route, handle_spotify_callback)]

    app = web.Application()

    app.add_routes(routes)
    web.run_app(app, port=port)
