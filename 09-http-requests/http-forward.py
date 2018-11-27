from sys import argv
import json
import urllib.request
import http.server


def wrap_handler(url):
    class RequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            target_url = 'http://' + url if url[:4] != 'http' else url
            headers = dict(self.headers)
            request = urllib.request.Request(url=target_url,
                                             headers=headers,
                                             data=None)
            try:
                response = urllib.request.urlopen(url=request,
                                                  timeout=1)
                content = self.process_response_from_server(response)
                return self.send_response_to_client(content)
            except urllib.error.URLError:
                print("Request has timeouted")
                content = json.dumps({"code": "timeout"}, indent=2)
                return self.send_response_to_client(content)
            except urllib.error.HTTPError as e:
                print("Request has an error")
                content = json.dumps({"code": e.code}, indent=2)
                return self.send_response_to_client(content)

        def do_POST(self):
            # Kindly borrowed from https://stackoverflow.com/a/5976905/6838293
            content_len = int(self.headers.get('content-length', 0))
            post_body = self.rfile.read(content_len)

            try:
                json_body = json.loads(post_body)
            except ValueError:
                content = json.dumps({"code": "invalid json"}, indent=2)
                return self.send_response_to_client(content)
            if "type" not in json_body or \
                "url" not in json_body or \
                (json_body["type"] == "POST" and "content" not in json_body):
                    content = json.dumps({"code": "invalid json"}, indent=2)
                    return self.send_response_to_client(content)
            method = json_body["type"]
            url = json_body["url"]
            headers = json_body["headers"] if "headers" in json_body else dict()
            content = json_body["content"] if method == "POST" else None
            if content:
                content = json.dumps(content).encode()
            timeout = json_body["timeout"] if "timeout" in json_body else 1

            request = urllib.request.Request(url=url,
                                             data=content,
                                             headers=headers)
            try:
                response = urllib.request.urlopen(request, timeout=timeout)
                content = self.process_response_from_server(response)
                return self.send_response_to_client(content)
            except urllib.error.URLError:
                print("Request has timeouted")
                content = json.dumps({"code": "timeout"})
                return self.send_response_to_client(content)
            except urllib.error.HTTPError as e:
                print("Request has an error")
                content = json.dumps({"code": e.code})
                return self.send_response_to_client(content)

        def process_response_from_server(self, response):
            response_dict = {}
            response_dict['code'] = response.status
            response_dict['headers'] = dict(response.getheaders())
            response_content = response.read().decode('utf-8')
            try:
                response_body = json.loads(response_content)
                response_dict['json'] = response_body
            except ValueError:
                response_dict['content'] = response_content
            return json.dumps(response_dict, indent=2)

        def send_response_to_client(self, content):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content.encode())
    return RequestHandler


def main():
    if len(argv) != 3:
        print('Enter port and server!')
        exit(1)
    port = argv[1]
    upstream = argv[2]
    listening_address = ('localhost', int(port))
    handler = wrap_handler(upstream)
    httpd = http.server.HTTPServer(server_address=listening_address,
                                   RequestHandlerClass=handler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
