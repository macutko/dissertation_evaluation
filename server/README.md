# Running the server localy

To run type npm run dev and that should start nodemon on the server. It would run on your local PC, so that means you have to connect you client onto the same network as the server. 
There is a util run_wifi.bat that runs a Wifi on your laptop.That gives confidence that your device is connected to thhe same LAN. To get the IP on which this runs just get the IPv4 
from ipconfig of your adapter that is currently on WAN (either eth or Wifi). The port is by default 12345 set in the config file

# Accessing the shared dev server. 

the shared server DDNS is on domacanas.hopto.org:12358
For security reasons I will always update this server with the most uptodate version of the code, but this server shouldnt be used as a dev server, rather a test server. 

