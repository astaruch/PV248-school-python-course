#!/bin/bash

curl -X GET 'http://localhost:9000/start'
curl -X GET 'http://localhost:9000/play?game=0&player=1&x=1&y=1' #[1,1]
curl -X GET 'http://localhost:9000/play?game=0&player=2&x=2&y=1' #[2,1]
curl -X GET 'http://localhost:9000/play?game=0&player=1&x=0&y=0' #[0,0]
curl -X GET 'http://localhost:9000/play?game=0&player=2&x=2&y=0' #[2,0]
curl -X GET 'http://localhost:9000/play?game=0&player=1&x=2&y=2' #[2,2] WIN

curl -X GET 'http://localhost:9000/play?game=0&player=2&x=1&y=2' #[2,2] END


curl -X GET 'http://localhost:9000/status?game=0' # WIN 1
