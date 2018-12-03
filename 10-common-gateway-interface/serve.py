from sys import argv
import http.server
import os
import socketserver


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass


def wrap_handler():
    class RequestHandler(http.server.CGIHTTPRequestHandler):
        """ Modify cgi_directories to accepts current directory"""
        def __init__(self, *args, **kwargs):
            super(self.__class__, self).__init__(*args, **kwargs)
            print('cwd: ', os.getcwd())
            cwd = os.getcwd().split(os.path.sep)[-1]
            cgi_dir = '/' + cwd
            print('Appending {} to "cgi_directories"...'.format(cgi_dir))
            self.cgi_directories.append(cgi_dir)

        def do_HEAD(self):
            self.do_REQUEST()

        def do_GET(self):
            self.do_REQUEST()

        def do_POST(self):
            self.do_REQUEST()

        def do_REQUEST(self):
            print("Request = ", self.path)
            """Test whether self.path corresponds to a CGI script."""
            if os.path.splitext(self.path)[1] == '.cgi' and self.is_cgi():
                """Serve a POST request."""
                self.run_cgi()
            else:
                """Serve a GET request."""
                f = http.server.SimpleHTTPRequestHandler.send_head(self)
                if f:
                    try:
                        self.copyfile(f, self.wfile)
                    finally:
                        f.close()
    return RequestHandler


def main():
    if len(argv) != 3:
        print('Enter port and directory to serve!')
        exit(1)

    port = argv[1]
    directory_name = argv[2]
    os.chdir(os.path.realpath(directory_name))
    listening_address = ('localhost', int(port))
    handler = wrap_handler()
    httpd = Server(server_address=listening_address,
                   RequestHandlerClass=handler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()