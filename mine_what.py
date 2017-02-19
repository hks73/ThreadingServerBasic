import sys
import base64
import http.server
from socketserver import ThreadingMixIn
import threading
from urllib.parse import urlparse
import time

key = "45"
HOST_NAME = "localhost"
PORT_NUMBER = 8012
import json

class AuthHandler(http.server.BaseHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
        print("send header")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print("send header")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global key
        header = self.headers.get_all('Authorization')
        if header == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received\n'.encode())
            pass
        elif ''.join(header) == 'Basic '+key:
            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in query.split("&"))
            print(query_components)
            delay = query_components["delay"]
            increment = query_components["increment"]

            username="Temp"
            response_data = {"username":username,"delay":delay+" seconds","counter":increment}
            json_data = json.dumps(response_data)
            time.sleep(int(delay))
            self.send_response(200,response_data)
            self.wfile.write(json_data.encode())
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(str(self.headers.get_all('Authorization')).encode())
            self.wfile.write('not authenticated\n'.encode())
            pass

class ThreadedHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    """Handle requests in a separate thread."""
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port

    server = ThreadedHTTPServer((HOST_NAME, PORT_NUMBER), AuthHandler)
    print('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()


    # # Start a thread with the server -- that thread will then start one
    # # more thread for each request
    # server_thread = threading.Thread(target=server.serve_forever)
    # # Exit the server thread when the main thread terminates
    # server_thread.daemon = True
    # server_thread.start()
    # print "Server loop running in thread:", server_thread.name
