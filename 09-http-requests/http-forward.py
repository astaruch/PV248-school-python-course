from sys import argv
import socket
# from time import sleep
import re
import json


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
                content_length = re.search(b'content-length: (\\d+)', request).group(1).decode('utf-8')
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
        request_body_json = json.loads(request_body)
        print(request_body_json)

    print('Connecting to upstream...')
    upstream_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    upstream_socket.connect((upstream, 80))
    print('Sending...')
    upstream_socket.sendall(request)
    response = bytearray()
    while True:
        data = upstream_socket.recv(1024)
        if data:
            response.extend(data)
        else:
            print("I shouldnt be here")
    print(response.decode('utf-8'))


if __name__ == '__main__':
    main()
