from flask import Flask, render_template, session, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
app = Flask(__name__)

# use session
app.secret_key = 'secr3t'
app.config['SESSION_TYPE'] = 'filesystem'


class LoginForm(FlaskForm):
    username = StringField('username')


@app.route('/', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        action = request.form.get('action')
        print(action)
        if action in ['new', 'join']:
            return redirect('/form')
    return render_template('menu.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()
    if form.validate_on_submit():
        session['username'] = form.username.data
        # This is where I would go to the next page
        # return f"<h4> Welcome: {session['username']}"
        return redirect(url_for('board', player=session['username']))
        # TODO: How do I pass template
    return render_template('form.html', form=form)


@app.route('/board/<player>')
def board(player):
    return render_template('board.html', player=player)


# https://medium.com/better-programming/building-your-first-website-with-flask-part-3-99df7d589078
