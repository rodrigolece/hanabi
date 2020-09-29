from flask import Flask, render_template, session, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from flask_socketio import SocketIO, send, emit  # broadcast

from simulated import simulated_game
from game import Hanabi


app = Flask(__name__)
# app.secret_key = 'secr3t'
app.config['SECRET_KEY'] = 'secr3t'
app.config['SESSION_TYPE'] = 'filesystem'  # use session
socketio = SocketIO(app)

debug_turn = False


@app.route('/')
def board():
    return render_template('board.html', player='rodrigo')


@socketio.on('connect')  # namespace='/test'
def send_board():
    if 'game' not in session:
        session['game'] = simulated_game()
        # session['game'] = Hanabi(2)
    emit('board', {'data': session['game'].serialise()})  # json=True


@socketio.on('played')
def parse_play(json):
    global debug_turn
    data = json['data']
    game = session['game']

    player, action, args = data['id'], data['action'], data['args']
    if debug_turn and player == game.current_player.index:
        app.logger.info('received json: ' + str(data))
        game.update_table(action, **args)
    elif debug_turn:
        send('Not your turn')
    else:
        app.logger.info('received json: ' + str(data))
        game.update_table(action, **args)


# class LoginForm(FlaskForm):
#     username = StringField('username', validators=[InputRequired()])


# @app.route('/', methods=['GET', 'POST'])
# def menu():
#     if request.method == 'POST':
#         action = request.form.get('action')
#         print(action)
#         if action in ['new', 'join']:
#             return redirect('/form')
#     return render_template('menu.html')
#
#
# @app.route('/form', methods=['GET', 'POST'])
# def form():
#     form = LoginForm()
#     if form.validate_on_submit():
#         session['username'] = form.username.data
#         return redirect(url_for('board', player=session['username']))
#     return render_template('form.html', form=form)
#
#
# @app.route('/board/<player>')
# def board(player):
#     return render_template('board.html', player=player)


# https://medium.com/better-programming/building-your-first-website-with-flask-part-3-99df7d589078

if __name__ == '__main__':
    socketio.run(app)
