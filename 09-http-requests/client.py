import requests
from sys import argv


def main():
    if argv[1] == '1':
        """Forward GET"""
        url = "http://localhost:9001"

        payload = ""
        headers = {
            'cache-control': "no-cache",
            }

        response = requests.request("GET", url, data=payload, headers=headers)

        print(response.text)
    elif argv[1] == '2':
        """GET example"""
        url = "http://postman-echo.com/get"

        payload = ""
        headers = {
            'cache-control': "no-cache",
            }

        response = requests.request("GET", url, data=payload, headers=headers)

        print(response.text)
    elif argv[1] == '3':
        """Create request from POST data and forward it - GET"""
        """
        {
            "type": "GET",
            "url": "http://postman-echo.com/get",
            "headers":
            {
                "X-test": "python",
                "X-test345": 123
            },
            "timeout": 0.1
        }
        """
        url = "http://localhost:9001"

        payload = "{\n\t\"type\": \"GET\",\n\t\"url\": \"http://postman-echo.com/get\",\n\t\"headers\": \n\t{\n\t\t\"X-test\": \"python\",\n\t\t\"X-test2\": 123\n\t},\n\t\"timeout\": 5\n}"
        headers = {
            'Content-Type': "application/json",
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
    elif argv[1] == '4':
        """Create request from POST data and forward it - POST"""
        """
        {
            "type": "POST",
            "url": "http://postman-echo.com/post",
            "headers":
            {
                "X-test": "python",
                "X-test345": 123
            },
            "content":
            {
                "python": "testing forwarding POST"
            },
            "timeout": 5
        }
        """
        url = "http://localhost:9001"
        payload = "{\r\n    \"type\": \"POST\",\r\n    \"url\": \"http://postman-echo.com/post\",\r\n    \"headers\":\r\n    {\r\n        \"X-test\": \"python\",\r\n        \"X-test345\": 123,\r\n\t    \"content-length\": \"37\",\r\n\t    \"content-type\": \"application/json\"\r\n    },\r\n    \"content\":\r\n    {\r\n        \"python\": \"testing forwarding POST\"\r\n    },\r\n    \"timeout\": 5\r\n}"
        headers = {
            'Content-Type': "application/json",
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)
    elif argv[1] == '5':
        """POST example"""
        url = "https://postman-echo.com/post"

        payload = "{ \"key\": \"param\" }"
        headers = {
            'Content-Type': "application/json",
            }

        response = requests.request("POST", url, data=payload, headers=headers)

        print(response.text)


if __name__ == '__main__':
    main()
