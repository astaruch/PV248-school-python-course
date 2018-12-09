#!/bin/bash

curl -X GET 'http://localhost:9000/start'
curl -X GET 'http://localhost:9000/play?game=0&player=1&x=1&y=1' #[1,1]
curl -X GET 'http://localhost:9000/play?game=0&player=2&x=1&y=1' #[1,1]

# "message": "Player 2 is on a turn."