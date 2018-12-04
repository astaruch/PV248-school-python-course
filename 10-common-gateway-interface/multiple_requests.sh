#!/bin/bash

curl -X GET http://localhost:9001/long-request.py.cgi &
curl -X GET http://localhost:9001/sample-file.txt &
curl -X GET http://localhost:9001/ &
curl -X GET http://localhost:9001/example.py.cgi &
curl -X GET http://localhost:9001/subdir &
curl -X GET http://localhost:9001/subdir/example.py.cgi &
curl -X POST \
  http://localhost:9001/hello_get.py.cgi \
  -H 'Postman-Token: 9c9245f4-3b95-4267-8221-1a5f02ec0511' \
  -H 'cache-control: no-cache' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F first_name=Andrej \
  -F last_name=Staruch &
  curl -X GET \
  'http://localhost:9001/hello_get.py.cgi?first_name=Andrej&last_name=Staruch' \
  -H 'Postman-Token: c195e990-cdc1-4c85-adbd-33f71642b987' \
  -H 'cache-control: no-cache' &