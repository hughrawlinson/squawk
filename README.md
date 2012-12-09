# Squawk
Squawk is a Twitter inspired web server that runs on a Raspberry PI and allows you to control your GPIOs remotely.
 
It was developed by Hugh Rawlinson [@hughrawlinson](http://www.twitter.com/hughrawlinson) and Rich Hollis [@richhollis](http://www.twitter.com/richhollis) at Code Club's Raspberry PI Hack (8/12/12 - 9/12/12). We won the best school focussed app prize.
 
Hey, why not just use the Twitter API? We originally considered talking directly to Twitter but we considered the possibility that some schools will block access to social media sites like Twitter through their firewall. So we decided to create a stand-alone project that anyone could use without restriction.
 
Squawk currently contains basic actions to turn on and off individual GPIO ports. For example, kids can squawk the following actions to turn GPIO 17 & 22 on and off:

TURN 17 ON

TURN 22 ON

TURN 22 OFF

We plan to add other actions in the future and make it easier to add other commands that you might want to control . We'd love to hear your suggestions on how we might make Squawk better for you and your class.
 
Squawk runs as a single python script. Currently, the only library dependency is CherryPy which is used to create the web server. The script needs run as sudo or your PI needs to be configured to allow access to the GPIO ports for another user.

# How To
Squawk is a python webserver that uses the [Cherry Py](http://cherrypy.org) library, so prior to using Squawk you'll have to install that. Instructions are at the Cherry Py website. To run squawk, go to the directory into which you downloaded the source and run `sudo python squawk.py`. It will set up the GPIO pins for you. On line 227 of Squawk you will have to put in the internal IP address of your Pi on your network. You can then set up port forwarding on your router to allow external access. You can then have any computer on the network point their browsers at the Pi port 8080 (you may want to set up dns or hosts files to use a domain name internally). Each user will be able to see each other's tweets, and command the GPIO ports (with the commands listed above)