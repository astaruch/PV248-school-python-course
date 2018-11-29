from sys import argv
import json
import urllib.request
import http.server
import os
import socketserver


def wrap_handler(path):
    class RequestHandler(http.server.CGIHTTPRequestHandler):
        # def do_HEAD(self):
        #     pass

        # def do_GET(self):
        #     pass

        # def do_POST(self):
        #     pass
        pass
        print(path)
    return RequestHandler


def main():
    if len(argv) != 3:
        print('Enter port and directory to serve!')
        exit(1)
    port = argv[1]
    directory_name = argv[2]
    serving_path = os.path.join(os.path.dirname(__file__), directory_name)
    print(serving_path)
    os.chdir(serving_path)
    listening_address = ('localhost', int(port))
    handler = wrap_handler(serving_path)
    httpd = socketserver.TCPServer(server_address=listening_address,
                                   RequestHandlerClass=handler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
