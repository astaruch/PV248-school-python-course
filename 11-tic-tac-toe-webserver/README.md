# Tic Tac Toe

write a game server for (3x3) tic tac toe
- invocation: ./ttt.py port
- listen on the given port (number)
- serve HTTP (only GET requests)
- all responses are JSON dictionaries

: Start
- GET /start?name=string
- returns a numeric id
- multiple games may run in parallel
- the game starts with an empty board
- player 1 plays ϐirst

Status
- GET /status?game=id
- if the game is over:
- set winner to 0 (draw), 1 or 2
- otherwise set:
- board is a list of lists of numbers
- 0 = empty, 1 and 2 indicate the player
- next 1 or 2 (who plays next)

 Tic Tac Toe Client
- include ttt.py from exercise 11
- add a /list request
- returns a JSON list of games
- each is a dict with name and id
- invocation: client.py host port