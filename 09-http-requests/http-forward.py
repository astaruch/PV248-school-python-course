from sys import argv
import socket
import re
import json
import urllib.request

# TODO: handle ssl
# TODO: force and handle it Accept-Encoding: Identity


def receive_request(sock):
    # TODO: parse headers and forward them correctly
    # TODO: possible change this for http.server library
    # TODO: test request with size moar than 1024 to test my shitty loop
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


def process_response(response):
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


def process_get_request(upstream_host, timeout=1):
    # TODO: handle forwarding of headers
    # TODO: edit check for http/https
    print('Connecting to upstream...')
    if upstream_host[:4] != 'http':
        url = 'http://' + upstream_host
    else:
        url = upstream_host
    try:
        response = urllib.request.urlopen(url=url, timeout=timeout)
    except (socket.timeout, urllib.error.URLError):
        print("Request has timeouted")
        return json.dumps({"code": "timeout"})
    return process_response(response)


def process_post_request(upstream, content_to_process):
    print(content_to_process)
    body = json.loads(content_to_process)
    if "type" in body:
        method = body["type"]
    else:
        return json.dumps({"code": "invalid json"})
    if "url" in body:
        url = body["url"]
    else:
        return json.dumps({"code": "invalid json"})
    if "headers" in body:
        headers = body["headers"]
    else:
        headers = dict()
    if method == "POST":
        if "content" in body:
            content = body["content"]
        else:
            return json.dumps({"code": "invalid json"})
    else:
        content = None
    if "timeout" in body:
        timeout = body["timeout"]
    else:
        timeout = 1
    print('Connecting to upstream...')
    if method == 'GET':
        # TODO: handle headers
        return process_get_request(url, timeout)
    elif method == 'POST':
        request = urllib.request.Request(url=url)
        for header_name, header_value in headers.items():
            request.add_header(header_name, header_value)
        content = json.dumps(content).encode()
        try:
            response = urllib.request.urlopen(request, data=content,
                                              timeout=timeout)
        except (socket.timeout, urllib.error.URLError):
            print("request has timeouted")
            return json.dumps({"code": "timeout"})
        return process_response(response)
    else:
        # TODO: handle this situation
        pass


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

    if request["method"] == 'POST':
        response_json = process_post_request(upstream, request["content"])
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
