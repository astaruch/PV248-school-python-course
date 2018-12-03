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


if __name__ == '__main__':
    main()
