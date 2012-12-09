import cherrypy
import re
import os
from datetime import datetime
from ossaudiodev import open

class SquawkApp(object):
    """Main Squawk Server"""

    def __init__(self):
        """Initialise Squawk Server"""
        self.squawkList = []
        print("initialised")
        os.system("echo \"17\" > /sys/class/gpio/export")
        os.system("echo \"22\" > /sys/class/gpio/export")
        os.system("echo \"out\" > /sys/class/gpio/gpio17/direction")
        os.system("echo \"out\" > /sys/class/gpio/gpio22/direction")
    
    def index(self):
        """Concatenate parts of web page"""
        return(self.header()+self.actions()+self.messages()+self.footer())
    index.exposed = True

    # def squawksJson(self):
    #   # serve json of all squawks after time
    #   retstr = ""
    #   for squawk in self.squawkList:
    #       retstr = retstr+"{name:"+squawk.username+",squawk:"+squawk.squawk+"time:"+str(squawk.time)+"}"
    #   return(retstr)
    # squawksJson.exposed = True

    def handleGPIOCommands(self,message):
        """Check message for GPIO command"""
        onGpio = GpioCommands.get_turn_on_gpio(message)
        offGpio = GpioCommands.get_turn_off_gpio(message)
        if(onGpio > 0):
            os.system("echo \"1\" > /sys/class/gpio/gpio"+str(onGpio)+"/value")

        if(offGpio > 0):
            os.system("echo \"0\" > /sys/class/gpio/gpio"+str(offGpio)+"/value")

    def postSquawk(self,name=None,message=None,avatar=None):
        """Prepend squawk input to squawkList"""
        self.handleGPIOCommands(message)
        squawk = Squawk(message,name)
        self.squawkList.insert(0,squawk)
        raise cherrypy.HTTPRedirect("/")
    postSquawk.exposed = True

    def header(self):
        """Return head of HTML"""
        # span{font-family:"Hevletica Neue",Helvetica,Arial,sans-serif}
        return('''<html>
<head>

<link href='http://fonts.googleapis.com/css?family=Geo' rel='stylesheet' type='text/css'>

<style>
body {
  text-align: center;
  background-image: url('https://raw.github.com/hughrawlinson/squawk/master/debut_dark.png'); 
  margin: 0;
  }

#container {
  margin: 0 auto;
  width: 920px;
  opacity: 0.9;
  }
  #container:after { clear: both;}

  #header { background-image: url('https://raw.github.com/hughrawlinson/squawk/master/twinkle_twinkle.png'); color: #888; text-align: left; height: 40px; font-family: 'Geo', sans-serif; font-size: 36px; letter-spacing: -4px; text-align: center;}

body{font-family:"Hevletica Neue",Helvetica,Arial,sans-serif;font-size:12pt;font-weight:300;}
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
.squawk { text-align: left; margin-bottom:0px;padding:8px;}
.squawk .submit {float: right;}
.submit{padding:0;margin:0;}
input{margin-bottom:8px;}

.message { text-align: left; padding: 8px; border-radius: 2px; margin-bottom: 2px;height:50px;}
.message IMG { float:left; height:48px; width:48px; border: 1px solid silver; border-radius: 4px; }
.message .body { display: inline-block; vertical-align: top; margin-top: 4px; margin-left: 4px;}
.message .body .from { font-weight: bold; margin-left: 4px;}
.message .time { float: right;}

</style>

</head>

<body>

<div id="container">

<div id="header">
    Squawk
  </div>''')

    def actions(self):
        """return html send div"""
        # return action
        return('''<div id="actions">

  <div id="send">
    <form method="post" action="postSquawk" class="squawk">
    Name:
      <input type="text" name="name" />
      Message:
      <input type="text" name="message" />
      <input type="submit" class="submit"/>
      <br style="clear:both;">
    </form>
  </div>

</div>''')

    def messages(self):
        """Return message container with message details"""
        # return messages in html
        return('''<div id="messages-container">
  <div id="messages">
    %s
  </div>
</div>''' % self.messagedetail())

    def footer(self):
        """return foot of html"""
        return('''</div>
</body>
</html>''')

    def messagedetail(self):
        """Return each message in html"""
        output = ""
        for squawk in self.squawkList:
            output += '''<div class="message">
      <img src="http://www.raspberrypi.org/wp-content/uploads/2012/03/Raspi_Colour_R.png" />
      <div class="body">
        <span class="from">%s</span><br/><span class="body">%s</span>
      </div>
      <div class="time">%s</div>
    </div>''' % (squawk.username,squawk.squawk,self.prettydate(squawk.time))
        return output

    def prettydate(self,d):
        """Twitter style times"""
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
    """Individual Squawk object"""

    def __init__(self, squawkText, squawkName):
        self.squawk = squawkText
        self.username = squawkName
        self.time = datetime.utcnow()

class GpioCommands(object):
    """Class for Controlling GPIO"""
    def __init__(self, arg):
        super(GpioCommands, self).__init__()
        self.arg = arg

    @staticmethod
    def get_turn_on_gpio(str):
        """Regex expression for turning on LED"""
        m = re.search('^TURN\s(\d{1,2})\sON$', str, re.IGNORECASE)
        if m is not None:
            return int(m.group(1))
        return 0

    @staticmethod
    def get_turn_off_gpio(str):
        """Regex expression for turning off LED"""
        m = re.search('^TURN\s(\d{1,2})\sOFF$', str, re.IGNORECASE)
        if m is not None:
            return int(m.group(1))
        return 0

cherrypy.server.socket_host = '192.168.1.100'
#cherrypy.tree.mount(SquawkApp(),"/")
#cherrypy.engine.start()
#cherrypy.engine.block()
cherrypy.quickstart(SquawkApp())