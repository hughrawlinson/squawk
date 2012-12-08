import cherrypy
from datetime import datetime

class SquawkApp(object):
	"""docstring for SquawkApp"""
	squakList[] = Squawk[]
	def index(self):
		# serve index
	def squawksjson(self):
		# serve json of squawks
	def postSquawk(self,squawkText,squawkName):
		# 
		squawk = squawk(squawkText,squawkName)

class Squawk(object):
	"""docstring for Squawk"""
	squawk = ""
	username = ""
	time = ""
	def __init__(self, squawkText, squawkName):
		super(ClassName, self).__init__()
		self.squawk = squawkText
		self.username = squawkName
		self.time = datetime.time(datetime.now())

class GPIOIntegration(object):
	"""docstring for GPIOIntegration"""
	def function(self):
		print("Called")