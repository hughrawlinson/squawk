import cherrypy
import re
import os
from datetime import datetime

class SquawkApp(object):
	"""docstring for SquawkApp"""
	s = Sound() 
	s.read('squawk2.aif') 

	def __init__(self):
		self.squawkList = []
		print("initialised")
		os.system("echo \"17\" > /sys/class/gpio/export")
		os.system("echo \"22\" > /sys/class/gpio/export")
		os.system("echo \"out\" > /sys/class/gpio/gpio17/direction")
		os.system("echo \"out\" > /sys/class/gpio/gpio22/direction")
	
	def index(self):
		return(self.header()+self.actions()+self.messages()+self.footer())
	index.exposed = True

	# def squawksJson(self):
	# 	# serve json of all squawks after time
	# 	retstr = ""
	# 	for squawk in self.squawkList:
	# 		retstr = retstr+"{name:"+squawk.username+",squawk:"+squawk.squawk+"time:"+str(squawk.time)+"}"
	# 	return(retstr)
	# squawksJson.exposed = True

	def handleGPIOCommands(self,message):
		onGpio = GpioCommands.get_turn_on_gpio(message)
		offGpio = GpioCommands.get_turn_off_gpio(message)
		if(onGpio > 0):
			os.system("echo \"1\" > /sys/class/gpio/gpio"+str(onGpio)+"/value")
			s.play()

		if(offGpio > 0):
			os.system("echo \"0\" > /sys/class/gpio/gpio"+str(offGpio)+"/value")
			s.play()

	def postSquawk(self,name=None,message=None,avatar=None):
		self.handleGPIOCommands(message)
		squawk = Squawk(message,name)
		self.squawkList.insert(0,squawk)
		raise cherrypy.HTTPRedirect("/")
	postSquawk.exposed = True

	def header(self):
		return('''<html>
<head>

<style>
body {
  text-align: center;
  background-image: url('https://raw.github.com/hughrawlinson/squawk/master/debut_dark.png'); 
  margin: 0;
  }

#container {
  margin: 0 auto;
  width: 920px;
  background-color: white; opacity: 0.9;
  }
  #container:after { clear: both;}

  #header { background-image: url('https://raw.github.com/hughrawlinson/squawk/master/twinkle_twinkle.png'); color: #888; text-align: left; height: 30px;}

#actions { width: 280px; float:left; background-color: #666; padding: 10px; overflow: hidden;}
#messages-container { background-color: #666; padding: 10px; overflow: hidden;}
#send { margin-top: 10px; padding: 4px; border-radius: 6px; background-color: silver; }
#send input { display: block; }
#send input[type='text'] { width: 100%;}
#messages { border-radius: 6px; background-color: white; }
#gpio { background-color: white; padding: 10px; border-radius: 6px;}
.io { height: 10px; width: 10px; padding: 2px; content: '.'; display: inline-block;}
.io.on { background: #0a0; }
.io.off { background: #a00; }

.message { text-align: left; padding: 8px; border-radius: 2px; }
.message .avatar { float:left; }
.message .body { display: inline-block; vertical-align: top; margin-top: 4px;}
.message .body .from { font-weight: bold;}
.message .time { float: right;}

</style>

</head>

<body>

<div id="container">

<div id="header">
    Squawk
  </div>''')

	def actions(self):
		# return action
		return('''<div id="actions">

  <div id="gpio">
    <div class="io on"></div>
    <div class="io off"></div>
  </div>

  <div id="send">
    <form method="post" action="postSquawk">
    Name:
      <input type="text" name="name" />
      Message:
      <input type="text" name="message" />
      Avatar:
      <select name="avatar">
      <option>Default</option>
      </select>
      <input type="submit" />
    </form>
  </div>

</div>''')

	def messages(self):
		# return messages in html
		return('''<div id="messages-container">
  <div id="messages">
	%s
  </div>
</div>''' % self.messagedetail())

	def footer(self):
		return('''</div>
</body>
</html>''')

	def messagedetail(self):
		output = ""
		for squawk in self.squawkList:
			output += '''<div class="message">
      <img src="http://placehold.it/48x48" />
      <div class="body">
        <span class="from">%s</span><br/><span class="body">%s</span>
      </div>
      <div class="time">%s</div>
    </div>''' % (squawk.username,squawk.squawk,self.prettydate(squawk.time))
		return output

	def prettydate(self,d):
	    diff = datetime.utcnow() - d
	    s = diff.seconds
	    if diff.days > 7 or diff.days < 0:
	        return d.strftime('%d %b %y')
	    elif diff.days == 1:
	        return '1 day ago'
	    elif diff.days > 1:
	        return '{} days ago'.format(diff.days)
	    elif s <= 1:
	        return 'just now'
	    elif s < 60:
	        return '{} seconds ago'.format(s)
	    elif s < 120:
	        return '1 minute ago'
	    elif s < 3600:
	        return '{} minutes ago'.format(s/60)
	    elif s < 7200:
	        return '1 hour ago'
	    else:
	        return '{} hours ago'.format(s/3600)


class Squawk(object):
	"""docstring for Squawk"""

	def __init__(self, squawkText, squawkName):
		self.squawk = squawkText
		self.username = squawkName
		self.time = datetime.utcnow()

class GpioCommands(object):
	"""docstring for GpioCommands"""
	def __init__(self, arg):
		super(GpioCommands, self).__init__()
		self.arg = arg

	@staticmethod
	def get_turn_on_gpio(str):
		m = re.search('^TURN\s(\d{1,2})\sON$', str, re.IGNORECASE)
		if m is not None:
			return int(m.group(1))
		return 0

	@staticmethod
	def get_turn_off_gpio(str):
		m = re.search('^TURN\s(\d{1,2})\sOFF$', str, re.IGNORECASE)
		if m is not None:
			return int(m.group(1))
		return 0

cherrypy.server.socket_host = '192.168.1.100'
#cherrypy.tree.mount(SquawkApp(),"/")
#cherrypy.engine.start()
#cherrypy.engine.block()
cherrypy.quickstart(SquawkApp())