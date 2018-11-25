from sys import argv
import socket
import re
import json
import urllib.request


def receive_request(sock):
    data = bytearray()
    GET = b'GET'
    POST = b'POST'
    REQUEST_END = b'\r\n\r\n'
    while True:
        if len(data) >= 3:
            if data[:3] == GET:
                method = 'GET'
                # print('It is a GET request')
                if data[-4:] == REQUEST_END:
                    # print('Full request received.')
                    break
            elif data[:4] == POST:
                method = 'POST'
                # print('It is a POST request.')
                # print('Finding content length')
                content_length = re.search(b'content-length: (\\d+)', data,
                                           re.IGNORECASE).group(1).decode(
                                           'utf-8')
                print(int(content_length))
                content_length = int(content_length)
                body = data[-content_length:].decode('utf-8')
                break
        buffer = sock.recv(1024)
        if buffer:
            data.extend(buffer)
            # print(data)
        else:
            print('Full request received.')
            break
    return {
        "method": method,
        "data": data,
        "content": body if method == 'POST' else None
    }


def process_get_request(upstream_host):
    print('Connecting to upstream...')
    url = 'http://' + upstream_host
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
    return json.dumps(response_dict)


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

    (clientsocket, _) = serversocket.accept()
    print('Accepted a client connection.')

    request = receive_request(clientsocket)
    request_method = request["method"]
    request_body = request["content"]

    if request["method"] == 'POST':
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
    elif request["method"] == 'GET':
        response_json = process_get_request(upstream)
    else:
        print('Unexpected method')
    status_line = b"HTTP/1.1 200 OK\nContent-Type: application/json\n\n"
    clientsocket.sendall(status_line)
    clientsocket.sendall(response_json.encode())
    clientsocket.close()


if __name__ == '__main__':
    main()
