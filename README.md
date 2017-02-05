# Flask Backend

## Folder structure

- app
	- init__.py
	- data
		- store.db
	- reqs.py
- app.json
- Procfile
- requirements.txt
- run.py
- runtime.txt

### `run.py`

```python
#!usr/bin/python
from app import app
app.run(debug = True)
```

### `app/__init__.py`

```python
from flask import Flask  	# import Flask
app = Flask(__name__)		# Our app is an instance of Flask
from app import api		# Import API here, more files can be imported here
```

### `app/api`

- Imports

	```python
	from app import app
	from flask import jsonify, request
	
	import json
	import time
	import sqlite3
	```

- Data fromatter

	```python
	# Returns standard JSON formatted object with data, message and response code.
	def dataFormatter(code, message, data):
	resp = jsonify({
		'code': code,
		'message': message,
		'data': data
	})
	resp.status_code = code
	return resp
	```
	
- Routes without database

	- Example route

		```python
		# Returns the square of a passed number
		# Example, 
		@app.route('/number/<num>', methods=['GET'])
def square_method(num):
			try:
				sq = int(num) * int(num)
				ret = "Square of " + num + " is " + str(sq) + "."
				return dataFormatter(200, "Success.", ret)
			except:
				ret = "Error: Pass a number."
				return dataFormatter(400, "Bad request.", ret)
		```
	
	- For particulars

	```python
	@app.route('/<name>', methods=['GET', 'PUT', 'DELETE'])
	def personParticular(name):
	
		# http://localhost:5000/The%20Doctor
		# cause I'm too lazy to edit the json for numeric keys :P
	
		# put
		if request.method == 'PUT':
			ptodelete = {}
			for person in data:
				if person['name'] == name:
					ptodelete = person
			if ptodelete in data:
				data.remove(ptodelete)
			ptoins = json.loads(request.form.get('data', ''))
			data.append(ptoins)
			saveFile()
			return dataFormatter(200, "Put successful", ptoins)
	
		# delete
		if request.method == 'DELETE':
			ptodelete = {}
			for person in data:
				if person['name'] == name:
					ptodelete = person
			if ptodelete in data:
				data.remove(ptodelete)
				saveFile()
				return dataFormatter(200, "delete successful", data)
			return dataFormatter(404, "Not found", [])
	
		# get
		if request.method == 'GET':
			psearch = {}
			for person in data:
				if person['name'] == name:
					psearch = person
			if psearch in data:
				return dataFormatter(200, "Person found", psearch)
			return dataFormatter(404, "Not found", [])

	```
	