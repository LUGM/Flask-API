from flask import Flask # import Flask module
app = Flask(__name__)	# Create a new object
from app import api		# import the api 'file'