from app import app
from flask import jsonify, request

import json

import sqlite3

password = "TOP_SECRET_CODE"

# Returns a JSON formatted data with a HTTP status code
def dataFormatter(code, message, data):
	resp = jsonify({
			'code': code,
			'message': message,
			'data': data
		})
	resp.status_code = code
	return resp

@app.route('/student', methods=['GET', 'POST'])
def getStudents():

	# GET the student information
	if request.method == 'GET':

		try:
			conn = sqlite3.connect('data/univ.db')

			# Check if the args have 'name' then query for the name, else retuen everything
			# curl -X GET "127.0.0.1:5000/student?name=Duan"
			# curl -X GET "127.0.0.1:5000/student"
			try:
				qname = request.args.get('name')
				print "Queried for " + str(qname)
				cursor = conn.execute("SELECT * FROM Student WHERE name = (?) ORDER BY ID", (qname, ))
			except:
				cursor = conn.execute("SELECT * FROM Student ORDER BY ID")

			students = []

			# Add to the list
			for row in cursor:
				stud = {}
				stud['ID'] = row[0]
				stud['name'] = row[1]
				stud['dept_name'] = row[2]
				stud['tot_cred'] = row[3]
				students.append(stud)

			message = "Success. Found " + str(len(students)) + " students."

			return dataFormatter(200, message, students)

		except:
			return dataFormatter(404, "Not found!", [])

		finally:
			conn.close()

	# POSTing student information
	# curl -X POST "127.0.0.1:5000/student" -H "Authorization:TOP_SECRET_CODE" -F "name=Tom" -F "ID=18899" -F "dept_name=English" -F "tot_cred=89"
	elif request.method == 'POST':

		# Pseudo authorization.
		try:
			sentpass = request.headers.get('Authorization')
			print "Sent pass = " + str(sentpass) 
			if (sentpass != password):
				return dataFormatter(401, "Unauthorized", [])
		except:
			return dataFormatter(400, "Bad request. Specify Header.", [])

		try:
			conn = sqlite3.connect('data/univ.db')

			try:
				
				qID = request.form.get('ID')
				qname = request.form.get('name')
				qdeptName = request.form.get('dept_name')
				qtotCred = request.form.get('tot_cred')
				
				# Check if the ID is present in the database.
				# Note that if the database is created systematically, it will fail to insert, but better check so you can return a customized message to the user.
				cursor = conn.execute("SELECT * FROM Student WHERE ID = (?)", (qID, ))

				studs = []
				for row in cursor:
					studs.append(row[0])
				if len(studs) > 0:
					return dataFormatter(409, "Already present", [])

				# Try to insert
				try:
					cursor = conn.execute("INSERT INTO Student (ID, name, dept_name, tot_cred) VALUES (?, ?, ?, ?)", (qID, qname, qdeptName, qtotCred, ))
					# Important: Push changes to the database
					conn.commit()
					return dataFormatter(201, "Inserted successfully.", [])

				except:
					conn.close()
					return dataFormatter(500, "Internal server error.", [])

			except:
				return dataFormatter(400, "Unauthorized. Need fields.", [])

		except:
			return dataFormatter(404, "Unable to connect.", [])

		finally:
			conn.close()



# # ------ # #

# Open the given json file in data.
with open('data/people.json') as data_file:
	data = json.load(data_file)

# Update the json file.
def saveFile():
	with open('data/people.json', 'w') as outfile:
		json.dump(data, outfile)

# # ------ # #

@app.route('/', methods=['GET'])
def personList():
	# Return data
	return dataFormatter(200, "Success", data)

@app.route('/favs', methods=['GET'])
def getFavs():
	# Return favs from data.
	return "" #	This exercise is left for the user.

@app.route('/add', methods=['POST'])
def addPerson():
	name = request.form.get('name', '')
	location = request.form.get('location', '')
	status = request.form.get('status', '')
	new_person = {
		'name': name, 
		'location': location, 
		'status': status,
		'isFav': False,
		'isNew': True
		}
	data.append(new_person)
	return dataFormatter(201, "Successfully added", data)

# # ------- # #

# Updated number with JSON formatting
@app.route('/number/<num>', methods=['GET'])
def square_method(num):
	try:
		sq = int(num) * int(num)
		ret = "Square of " + num + " is " + str(sq) + "."
		return dataFormatter(200, "Success.", ret)
	except:
		ret = "Error: Pass a number."
		return dataFormatter(400, "Bad request.", ret)


@app.route('/', methods=['GET'])
def mainRoute():
	return "Hello World!"


@app.route('/string/<string>', methods=['GET', 'POST'])
def string_method(string):
	# GET
	if (request.method == 'GET'):
		return "You're GETting it, " + string + "!"

	# POST
	elif (request.method == 'POST'):
		return "Stop POSTing it, " + string.upper() + "!"
