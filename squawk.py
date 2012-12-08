import cherrypy
from datetime import datetime

class SquawkApp(object):
	"""docstring for SquawkApp"""

	def __init__(self):
		self.squawkList = []
	
	def index(self):
		return("index works")

	def squawksjson(self,time):
		# serve json of all squawks after time
		for squawk in squawkList[]:
			print("{name:"+squawk.username+",squawk:"+squawk.squawk+"time:"+squawk.time+"}")

	def postSquawk(self,squawkText=None,squawkName=None):
		squawk = squawk("This is the very first Squawk","Hugh")
		self.squawkList.append(squawk)

class Squawk(object):
	"""docstring for Squawk"""

	def __init__(self, squawkText, squawkName):
		super(ClassName, self).__init__()
		self.squawk = squawkText
		self.username = squawkName
		self.time = datetime.time(datetime.now())

class GPIOIntegration(object):
	"""docstring for GPIOIntegration"""

	def function(self):
		print("Called")