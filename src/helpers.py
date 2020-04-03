"""
A module with helper functions
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (helpers.py) is part of AsyncSpotify which is released under MIT.                     #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process
from time import sleep


class SetupServer:
    """
    Class which can be used to create a callback server
    """

    server_instance: Process = None

    @classmethod
    def setup_class(cls):
        """
        Create the callback server
        """

        cls.server_instance = Process(target=cls.run_server)
        cls.server_instance.start()
        sleep(1)

    @classmethod
    def teardown_class(cls):
        """
        Close the callback server
        """

        cls.server_instance.kill()

    @classmethod
    def run_server(cls):
        """
        Actually create the callback server
        """

        server_address = ('', 1234)
        httpd = HTTPServer(server_address, CustomHTTPHandler)
        httpd.serve_forever()


class CustomHTTPHandler(BaseHTTPRequestHandler):
    """
    Custom HTTP Handler without logging
    """

    def do_GET(self):
        """
        Handle GET requests
        """

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(bytearray())

    def do_HEAD(self):
        """
        Handle HEAD requests
        """

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytearray())

    def do_POST(self):
        """
        Handle POST requests
        """

        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytearray())

    def log_message(self, *__):
        """
        Suppress logging
        """
        return
