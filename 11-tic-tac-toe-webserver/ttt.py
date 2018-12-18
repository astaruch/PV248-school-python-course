from sys import argv
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
import json


def wrap_handler():
    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            print(self.path)
            parsed = urlparse.urlsplit(self.path)

            action = parsed.path[1:]
            params = urlparse.parse_qs(parsed.query)
            if action == 'start':
                name = params['name'][0] if 'name' in params else ''
                return self.start_game(name)
            elif action == 'status':
                if 'game' not in params:
                    return self.invalid_request(
                        code=400,
                        status='bad',
                        message='Missing parameter: game')
                try:
                    game_id = int(params['game'][0])
                except ValueError:
                    return self.invalid_request(
                        code=400,
                        status='bad',
                        message='Wrong parameter (non-integer): game'
                    )
                return self.state_of_game(game_id)
            elif action == 'play':
                if 'game' not in params or \
                   'player' not in params or \
                   'x' not in params or \
                   'y' not in params:
                    return self.invalid_request(
                        code=400,
                        status='bad',
                        message='Missing parameter'
                    )
                try:
                    game_id = int(params['game'][0])
                    player_id = int(params['player'][0])
                    x = int(params['x'][0])
                    y = int(params['y'][0])
                except ValueError:
                    return self.invalid_request(
                        code=400,
                        status='bad',
                        message='Wrong parameter (non-integer)'
                    )
                return self.play_turn(game_id, player_id, x, y)
            elif action == 'list':
                return self.list_games()
            else:
                return self.invalid_request(
                    code=404,
                    status='bad',
                    message='Invalid action requested (start|status|play|list)'
                )

        class Game():
            def __init__(self, name, game_id):
                self.board = [[0, 0, 0],
                              [0, 0, 0],
                              [0, 0, 0]]
                self.winner = -1
                self.next_player = 1
                self.game_id = game_id
                self.name = name
                self.total_turns = 0

            def get_state(self):
                if self.winner != -1:
                    return json.dumps({'winner': self.winner}, indent=2)
                response = {
                    'board': self.board,
                    'next': self.next_player
                }
                return json.dumps(response)

            def check_victory(self, player_id, x, y):
                # borrowed from https://codereview.stackexchange.com/a/24890
                # check if previous move caused a win on vertical line
                if self.board[0][y] == \
                   self.board[1][y] == \
                   self.board[2][y] == \
                   player_id:
                    return True

                # check if previous move caused a win on horizontal line
                if self.board[x][0] == \
                   self.board[x][1] == \
                   self.board[x][2] == \
                   player_id:
                    return True

                # check if previous move caused a win on diagonal line
                if self.board[0][0] == \
                   self.board[1][1] == \
                   self.board[2][2] == \
                   player_id:
                    return True

                # check if previous move caused a win on diagonal line
                if self.board[0][2] == \
                   self.board[1][1] == \
                   self.board[2][0] == \
                   player_id:
                    return True
                return False

            def play_turn(self, player_id, x, y):
                if self.winner != -1:
                    if self.winner == 0:
                        message = "It's a draw."
                    else:
                        message = "Player {} won.".format(self.winner)
                    return (False, 'The game has ended. {}'.format(message))
                if player_id != self.next_player:
                    return (False,
                            'Player {} is on a turn.'.format(self.next_player))
                if self.board[x][y] != 0:
                    return (False,
                            'Cell [{},{}] is already taken.'.format(x, y))
                self.next_player = 1 if player_id == 2 else 2
                self.board[x][y] = player_id
                self.total_turns += 1

                if self.check_victory(player_id, x, y):
                    self.winner = player_id
                elif self.total_turns == 9:
                    # The board is full and nobody had won - it's a draw
                    self.winner = 0

                return (True, '')

        games = []

        def start_game(self, name):
            print('New game created. game_id = {}'.format(len(self.games)))
            new_game = self.Game(name, len(self.games))
            self.games.append(new_game)
            response = json.dumps({'id': new_game.game_id}, indent=2)
            return self.send_response_to_client(200, response)

        def list_games(self):
            response = []
            for game in self.games:
                response.append({'id': game.game_id, 'name': game.name})
            response = json.dumps(response, indent=2)
            return self.send_response_to_client(200, response)

        def state_of_game(self, game_id):
            print('Requested status of a game: {}'.format(game_id))
            if game_id >= len(self.games) or game_id < 0:
                return self.invalid_request(
                    code=400,
                    status='bad',
                    message='Non-existing game requested')
            return self.send_response_to_client(
                code=200,
                body=self.games[game_id].get_state()
            )

        def play_turn(self, game_id, player_id, x, y):
            print('Game {}. Player {} playing [{},{}].'.format(
                game_id, player_id, x, y))
            # gameid špatné nebo chybí -- chybový kód
            if game_id >= len(self.games) or game_id < 0:
                return self.invalid_request(
                    code=400,
                    status='bad',
                    message='Non-existing game requested')
            if not (player_id == 1 or player_id == 2):
                return self.invalid_request(
                    code=200,
                    status='bad',
                    message='Invalid parameter: player')
            # Chybné (ale číselné) x nebo y: kód 200 + status bad.
            if x < 0 or x > 2:
                return self.invalid_request(
                    code=200,
                    status='bad',
                    message='Invalid parameter: x')
            # Chybné (ale číselné) x nebo y: kód 200 + status bad.
            if y < 0 or y > 2:
                return self.invalid_request(
                    code=200,
                    status='bad',
                    message='Invalid parameter: y')
            (play_ok, message) = self.games[game_id].play_turn(player_id, x, y)
            if play_ok:
                return self.send_response_to_client(
                    code=200,
                    body=json.dumps({'status': 'ok'}, indent=2)
                )
            else:
                return self.invalid_request(
                    code=200,
                    status='bad',
                    message=message
                )

        def send_response_to_client(self, code, body):
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body.encode())

        def invalid_request(self, code, status, message):
            response_dict = {
                "status": status,
                "message": message
            }
            response = json.dumps(response_dict, indent=2)
            self.send_response_to_client(code, response)

    return RequestHandler


def main():
    if len(argv) != 2:
        print('ENTER PORT')
        exit(1)
    port = argv[1]
    listening_address = ('localhost', int(port))
    handler = wrap_handler()
    httpd = HTTPServer(server_address=listening_address,
                       RequestHandlerClass=handler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
