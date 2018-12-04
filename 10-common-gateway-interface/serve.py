from sys import argv
import http.server
import os
import socketserver
import urllib.parse


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass


def wrap_handler():
    class RequestHandler(http.server.CGIHTTPRequestHandler):
        def do_HEAD(self):
            self.do_REQUEST()

        def do_GET(self):
            self.do_REQUEST()

        def do_POST(self):
            self.do_REQUEST()

        def do_REQUEST(self):
            """ Modify cgi_directories to accepts current directory"""
            curr_dir = os.path.dirname(self.path)
            if curr_dir not in self.cgi_directories:
                print('Appending "{}" into "cgi_directories"'.format(curr_dir))
                self.cgi_directories.append(curr_dir)

            """Test whether self.path corresponds to a CGI script."""
            filename = urllib.parse.urlparse(self.path).path[1:]
            if filename.endswith('.cgi') and self.is_cgi():
                print('Running cgi...')
                self.run_cgi()
            else:
                print('Serving as static content...')
                f = http.server.SimpleHTTPRequestHandler.send_head(self)
                if f:
                    try:
                        self.copyfile(f, self.wfile)
                    finally:
                        f.close()
    return RequestHandler


def main():
    if len(argv) != 3:
        print('ENTER PORT AND DIRECTORY')
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
