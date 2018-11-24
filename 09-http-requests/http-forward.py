from sys import argv
import socket
import re
import json
import urllib.request


def main():
    if len(argv) != 3:
        print('Enter port and server!')
        exit(1)
    port = argv[1]
    upstream = argv[2]
    listening_address = 'localhost'
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((listening_address, int(port)))
    serversocket.listen(1)
    print('Waiting for connection...')
    (clientsocket, address) = serversocket.accept()
    print('Clientsocket: ', clientsocket)
    print('Address:', address)
    request = bytearray()
    GET = b'GET'
    POST = b'POST'
    REQUEST_END = b'\r\n\r\n'
    while True:
        if len(request) >= 3:
            if request[:3] == GET:
                request_method = 'GET'
                print('It is a GET request')
                if request[-4:] == REQUEST_END:
                    print('Full request received. Going further..')
                    break
            elif request[:4] == POST:
                request_method = 'POST'
                print('It is a POST request...')
                print('Finding content length')
                content_length = re.search(b'content-length: (\\d+)',
                                           request).group(1).decode('utf-8')
                print(int(content_length))
                content_length = int(content_length)
                request_body = request[-content_length:].decode('utf-8')
                break
        data = clientsocket.recv(1024)
        if data:
            request.extend(data)
            # print(request)
        else:
            print('I dont know why I am here yet')
            break
    request_decoded = request.decode('utf-8')
    print(request_decoded)
    if (request_method == 'POST'):
        """
        {
            "type": "GET",
            "url": "http://postman-echo.com/get",
            "headers":
            {
                "X-test": "python",
                "X-test345": 123
            },
            "timeout": 5
        }
        """
        in_request = json.loads(request_body)
        out_request_type = in_request["type"]
        out_request_url = in_request["url"]
        out_request_headers = in_request["headers"]
        if out_request_type == "POST":
            out_request_type = in_request["content"]
        timeout = in_request["timeout"]
        print(in_request)
        print('Connecting to upstream...')
        out_request = bytearray()
        out_request.extend(("{} {} HTTP/1.1\n"
                            .format(out_request_type, out_request_url)
                            ).encode())
        print(out_request_headers.type)
        for header_name, value in out_request_headers.items():
            out_request.extend(("{}: {}\n".format(header_name, value)).encode())
        ## GET
        response = urllib.request.Request(url=out_request_url,

            )
        exit
    else:
        # GET
        print('Connecting to upstream...')
        url = 'http://' + upstream
        try:
            response = urllib.request.urlopen(url)
        except socket.timeout:
            # TODO: handle timeout
            print("Request has timeouted")
            pass
        response_dict = {}
        response_dict['code'] = response.status
        response_dict['headers'] = dict(response.getheaders())
        response_content = response.read().decode('utf-8')
        try:
            response_body = json.loads(response_content)
            response_dict['json'] = response_body
        except ValueError:
            response_dict['content'] = response_content
        print(response_dict)
        response_json = json.dumps(response_dict)
        # response_json_json = json.loads(response_json)
        response_bytes = bytearray()
        response_bytes.extend("HTTP/1.1 200 OK\n".encode())
        response_bytes.extend("Content-Type: application/json\n".encode())
        response_bytes.extend("\n".encode())
        response_bytes.extend(response_json.encode())
        clientsocket.sendall(response_bytes)
        clientsocket.close()


if __name__ == '__main__':
    main()
