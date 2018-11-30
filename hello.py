from flask import Flask
from flask import current_app
from flask import redirect
from flask import make_response
from flask import abort

app = Flask(__name__)

@app.route('/')
def index():
	return '<h1>Hello World!</h1>\n<h1>The app name is {0}</h1>'.format(current_app.name)

@app.route('/user/<name>')
def user(name):
	if name == 'google':
		return redirect('http://www.google.com')
	elif name == 'baidu':
		abort(404)
	elif name == 'Autodesk':
		response = make_response('<h1 style="color:red;">Welcome to Autodesk</h1>')
		return response
	else:
	    return '<h1>Hello {0}</h1>'.format(name)

if __name__ == '__main__':
	app.run(debug=True)
