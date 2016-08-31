from flask import Flask,request,render_template,g
import requests
import json
import collections

app = Flask(__name__)
# from query.details import details_module
# app.register_blueprint(details_module)

@app.route('/', methods=['GET'])
def index():
	if request.method == 'GET':		
		return render_template('loginform.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
	if request.method == 'GET':		
		return render_template('tables.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5001,debug=True)