from flask import Flask
from flask import current_app
from flask import redirect, url_for, flash
from flask import session
from flask import request
from flask import make_response
from flask import render_template
from flask import abort
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Idonotknow'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'appData.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mydb = SQLAlchemy(app)

class Role(mydb.Model):
    __tablename__ = 'roles'
    id = mydb.Column(mydb.Integer, primary_key=True)
    name = mydb.Column(mydb.String(64), unique=True)
    users = mydb.relationship('User', backref='role')

    def __repr__(self):
        return '<Role {0!r}>'.format(self.name)

class User(mydb.Model):
    __tablename__ = 'users'
    id = mydb.Column(mydb.Integer, primary_key=True)
    username = mydb.Column(mydb.String(64), unique=True, index=True)
    role_id = mydb.Column(mydb.Integer, mydb.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {0!r}>'.format(self.username)



class NameForm(FlaskForm):
    name = StringField('What\'s your name?', validators=[InputRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def index():
    return '<h1>Hello World!</h1>\n<h1>The app name is {0}</h1>'.format(current_app.name)

@app.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    if name == 'google':
        return redirect('http://www.google.com')
    elif name == 'baidu':
        abort(404)
    elif name == 'Autodesk':
        response = make_response('<h1 style="color:red;">Welcome to Autodesk</h1>')
        return response
    else:
        form = NameForm(request.form)
        # The following link tells why validate method always fails
        # https://stackoverflow.com/questions/20170234/validate-on-submit-always-returns-false-using-flask-wtforms?rq=1
        if form.validate_on_submit():
            old_name = session['name']
            if old_name is not None and old_name != form.name.data:
                flash('Looks like you have changed your name!')

            session['name'] = form.name.data
            form.name.data = ''
            return redirect(url_for('user', name=session.get('name')))
        if session.get('name') == None:
            return render_template('user.html', name=name, current_time=datetime.utcnow(), form=form)
        else:
            return render_template('user.html', name=session.get('name'), current_time=datetime.utcnow(), form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    #app.run(debug=True)
    manager.run()

