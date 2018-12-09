#!/bin/bash

# Should create a game
curl -X GET 'http://localhost:9000/start?name=some_name'

# Shouldn't crash and return error code (+msg)
curl -X GET 'http://localhost:9000/start?something=some_name'
curl -X GET 'http://localhost:9000/something_illegal?something=some_name'
curl -X GET 'http://localhost:9000/status?game=non_integer'
curl -X GET 'http://localhost:9000/status?game=0ahoj'
curl -X GET 'http://localhost:9000/play?game=0&x=0&y=0&player=-1'
curl -X GET 'http://localhost:9000/play?game=0&x=0&y=0&player=3'
curl -X GET 'http://localhost:9000/play?game=0&x=0&y=0&player=0'
curl -X GET 'http://localhost:9000/play?game=0&x=0&y=0'
curl -X GET 'http://localhost:9000/play?game=0&x=0&y=0&player=0'
curl -X GET 'http://localhost:9000/play?game=0&x=0&player=0'
curl -X GET 'http://localhost:9000/play?game=0&y=0&player=0'
curl -X GET 'http://localhost:9000/play?x=0&y=0&player=0'
curl -X GET 'http://localhost:9000/play?x=0&y=0&player=0'
curl -X GET 'http://localhost:9000/play?game=42&x=0&y=0&player=1'
curl -X GET 'http://localhost:9000/play?game=lul12&x=0&y=0&player=1'

