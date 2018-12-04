import requests
from sys import argv


def main():
    if argv[1] == '1':
        """GET example.py.cgi in served directory. Expect HTML, not python"""
        url = "http://localhost:9001/example.py.cgi"

        payload = ""
        headers = {}

        response = requests.request("GET", url, data=payload, headers=headers)

        print(response.text)
    elif argv[1] == '2':
        """GET served directory. Expect HTML, not 404."""
        url = "http://localhost:9001/"

        payload = ""
        headers = {}

        response = requests.request("GET", url, data=payload, headers=headers)

        print(response.text)
    elif argv[1] == '3':
        """GET sample-file.txt. Expect TXT, not HTML."""
        url = "http://localhost:9001/sample-file.txt"

        payload = ""
        headers = {}

        response = requests.request("GET", url, data=payload, headers=headers)

        print(response.text)
    elif argv[1] == '4':
        """GET hello_get.py.cgi without params. Expect:
        <html>
            <head>
                <title>Hello - Second CGI Program</title>
            </head>
            <body>
                <h2>Hello None None</h2>
            </body>
        </html>
        """
        url = "http://localhost:9001/hello_get.py.cgi"

        payload = ""
        headers = {}

        response = requests.request("GET", url, data=payload, headers=headers)

        print(response.text)
    elif argv[1] == '5':
        """GET hello_get.py.cgi with params. Expect:
        <html>
            <head>
                <title>Hello - Second CGI Program</title>
            </head>
            <body>
                <h2>Hello Andrej Staruch</h2>
            </body>
        </html>
        """
        url = "http://localhost:9001/hello_get.py.cgi"

        querystring = {"first_name": "Andrej", "last_name": "Staruch"}

        payload = ""
        headers = {}

        response = requests.request("GET", url, data=payload, headers=headers,
                                    params=querystring)

        print(response.text)
    elif argv[1] == '6':
        """POST hello_get.py.cgi with params. Expect:
        <html>
            <head>
                <title>Hello - Second CGI Program</title>
            </head>
            <body>
                <h2>Hello Andrej Staruch</h2>
            </body>
        </html>
        """
        url = "http://localhost:9001/hello_get.py.cgi"

        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"first_name\"\r\n\r\nAndrej\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"last_name\"\r\n\r\nStaruch\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'cache-control': "no-cache",
            'Postman-Token': "e4d979bf-7d0b-40d7-b1d2-457352d7d156"
            }

        response = requests.request("POST", url, data=payload, headers=headers)


if __name__ == '__main__':
    main()
