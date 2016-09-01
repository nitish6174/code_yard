from flask import Flask,request,render_template,session,redirect,url_for,escape
import requests
import json
import re

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
	if request.method == 'GET':
		if 'username' in session:
			return redirect(url_for('dashboard'))
		else:
			return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
	if 'username' in session:
		return redirect(url_for('dashboard'))
	else:
		if request.method == 'GET':
			return render_template('login.html')
		elif request.method == 'POST':
			login_username = request.form['username']
			login_password = request.form['password']
			if re.match(r'^team\d\d$',login_username)!=None and re.match(r'^\d{4}$',login_password)!=None:
				team_number = int(login_username[4:6])
				team_password = (1234+7383*team_number)%10000
				if team_password==int(login_password):
					session['username'] = request.form['username']
					return url_for("dashboard", _external=True)
			return url_for("login", _external=True)


@app.route('/dashboard', methods=['GET'])
def dashboard():
	if 'username' not in session:
		return redirect(url_for('login'))
	else:
		if request.method == 'GET':
			return render_template('dashboard.html')


@app.route('/logout', methods=['GET','POST'])
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))



app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000,debug=True)