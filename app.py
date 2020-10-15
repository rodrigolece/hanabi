from flask import Flask, render_template, session, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from flask_socketio import SocketIO, send, emit  # broadcast

# from simulated import simulated_game
from game import Hanabi


app = Flask(__name__)
# app.secret_key = 'secr3t'
app.config['SECRET_KEY'] = 'secr3t'
app.config['SESSION_TYPE'] = 'filesystem'  # use session
socketio = SocketIO(app)

game_pool = {}
id_new_game = 0


def new_game(nb_players):
    global id_new_game

    app.logger.info(f'Creating new game - nb players: {nb_players}')
    game_pool[id_new_game] = Hanabi(nb_players, seed=id_new_game)

    out = id_new_game
    # return the id of the new game, TODO: use this
    id_new_game += 1

    return out


def add_player_to_game(game_id, username):
    game = game_pool.get(game_id)
    if not hasattr(game, 'players_connected'):
        setattr(game, 'players_connected', {})

    connected = game.players_connected
    nb_conn = len(connected)

    if nb_conn < game.nb_players:
        connected[username] = nb_conn
    else:
        print('game is full')  # TODO: handle

    return None


# TODO: Below needs to be automated
game_id = new_game(2)


@app.route('/', methods=['GET', 'POST'])
def menu():
    username = session.get('username', None)
    if request.method == 'POST':
        action = request.form.get('action')

        if (username is None) and action in ['new', 'join']:
            return redirect('/form')

        elif action in ['new', 'join']:
            return redirect(url_for('board', username=username))

    return render_template('menu.html', username=username)


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('board', username=session['username']))

    return render_template('form.html', form=form)


@app.route('/delete-session')
def delete_session():
    session.clear()
    # session.pop('username')
    # session.pop('game_id')
    return 'session deleted'


@app.route('/board/<username>')
def board(username):
    if 'game_id' not in session:
        # TODO: choose game_id automatically
        session['game_id'] = game_id
        add_player_to_game(game_id, username)
        app.logger.info(f"Adding '{username}' to game: {game_id}")
    else:
        pass

    game = game_pool[game_id]
    connected = game.players_connected
    player = connected[username]

    return render_template('board.html', username=username, player=player)


@socketio.on('connect')  # namespace='/test'
def send_board():
    game = game_pool.get(session['game_id'])  # TODO: handle None
    emit('board', {'data': game.serialise()})


@socketio.on('played')
def parse_played(json):
    game = game_pool.get(session['game_id'])  # TODO: handle None
    data = json['data']
    player, action, args = data['id'], data['action'], data['args']

    if player == str(game.current_player.index):
        app.logger.info('received json: ' + str(data))
        game.update_table(action, **args)

        emit('board', {'data': game.serialise()}, broadcast=True)
    else:
        emit('alert', 'Not your turn')


if __name__ == '__main__':
    socketio.run(app)
