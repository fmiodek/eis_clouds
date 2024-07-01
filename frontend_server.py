import http.server
import socketserver
import os

"""
Frontend available on http://HOST:PORT/scores.html
"""

FRONTEND_PORT = 8000
FRONTEND_DIRECTORY = "./frontend"

# server for displaying frontend page
Handler = http.server.SimpleHTTPRequestHandler

# Change the current directory to serve files from the given directory
with socketserver.TCPServer(("", FRONTEND_PORT), Handler) as httpd:
    print("Serving at port", FRONTEND_PORT)
    # Change to the directory that contains your frontend files
    os.chdir(FRONTEND_DIRECTORY)
    # Start the server
    httpd.serve_forever()