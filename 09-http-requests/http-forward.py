from sys import argv
import socket
# from time import sleep
import http.server
import socketserver

def main():
    if len(argv) != 3:
        print('Enter port and server!')
        exit(1)
    port = argv[1]
    target_address = argv[2]
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
                print('It is a GET request')
                if request[-4:] == REQUEST_END:
                    print('Full request received. Going further..')
                    break
            elif request[:4] == POST:
                print('It is a POST request')
        data = clientsocket.recv(1024)
        if data:
            request.extend(data)
            print(request)
        else:
            print('I dont know why I am here yet')
            break






    pass


if __name__ == '__main__':
    main()
