"""
This file provides a callback server for the spotify auth process. It is intended for automated testing, so use it with
care.
"""

from multiprocessing import Process

from aiohttp import web
from multidict import MultiDictProxy
import multiprocessing

server_handler: multiprocessing.Pool = None


async def handle_spotify_callback(request):
    """
    Handle the redirection make by spotify after the oauth dialog
    :param request The request that spotify send with the redirect
    :return: json The code that spotify delivered
    """
    query_object: MultiDictProxy = request.query
    if "code" in query_object:
        return web.json_response({"code": query_object["code"]})

    return web.json_response({"error": "Could not get the response code from spotify"})


async def return_default(_):
    """
    Returns the default route
    :return: "success"
    """

    return web.json_response({"success", "created server"})


def make_server(port, callback_route) -> None:
    """
    Creates a server for the callback after the oauth dialogue
    :param callback_route: THe route that will be used as callback for spotify
    :param port: The port the server runs on
    :return: None
    """

    routes: list = [
        web.get("/", return_default),
        web.get(callback_route, handle_spotify_callback)
    ]

    app = web.Application()

    app.add_routes(routes)
    web.run_app(app=app, port=port)


def _create_callback_server(port: int, callback_route: str) -> Process:
    mp_context = multiprocessing.get_context('spawn')
    webserver_process = mp_context.Process(target=make_server, args=(port, callback_route))
    webserver_process.start()
    return webserver_process
