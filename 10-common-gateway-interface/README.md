# Common gateway interface

CGI
- invocation: ./serve.py 9001 dir
- listen on the speciϐied port (9001 in this case)
- serve the content of dir over HTTP
- treat ϐiles named .cgi specially (see next slide)
- serve anything else as static content

 Running CGI Scripts
- if a .cgi ϐile is requested, run it
- adhere to the CGI protocol
- request info goes into environment variables
- the stdout of the script goes to the client
- refer to RFC 3875 and/or Wikipedia
- do not forget to deal with POST request