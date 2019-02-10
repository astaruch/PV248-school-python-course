# Communication, HTTP

Forwarding HTTP
- invocation: ./http-forward.py 9001 example.com
- listen on the speciϐied port (9001 above) for HTTP
- use example.com as the upstream for GET
- for GET requests:
- forward the request as-is to the upstream
- send back JSON to your client (see next slide)
- for POST requests
- accept JSON data, construct request, proceed as GET
- supply suitable default headers unless overridden

: GET Requests
- the reply to the client must be valid JSON dictionary
- send the upstream response code as code
- or "timeout" (by default after 1 second)
- send all the received headers to the client
- if the response is valid JSON, include it under json
- include it as a string in content otherwise

POST Requests
- read a JSON dictionary from the request content; keys:
- type – string, either GET (default) or POST
- url – string, the address to fetch
- headers – dictionary, the headers to send
- content – the content to send if type is POST
- timeout – number of seconds to wait for completion
- if the JSON is invalid, set code to "invalid json"
- also if a crucial key is missing (url, content for POST)