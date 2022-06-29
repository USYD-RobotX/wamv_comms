#!/usr/bin/env python3

import rospy # ROS python module.
from std_msgs.msg import *
from sensor_msgs.msg import NavSatFix
import comms # Handles formatting of heartbeat & messages.


class _conman(): # Conman: connection manager. It automatically sends a heartbeat with GPS fix if available. 


    def __init__(self): # Initialise communication manager.
       
        print("conman started")
        ip = "localhost" # Not sure about this.
        if (rospy.has_param('/ip')):
                ip = rospy.get_param('/ip') # Get ROS IP address


        port = 2000 # Complete guess.
        if (rospy.has_param('/port')):
                port = rospy.get_param('/port') # Get ROS port.
        

        TMID = "XBZXC" # Needs to be set for 2022 team ID.
        if (rospy.has_param('/TID')):
                TMID = rospy.get_param('/TID') # Get team ID defined through ROS.
        

        mode=3 # Default mode = Killed.\
        # Get operating mode if defined through ROS, else assume killed.
        if (rospy.has_param('/mode')):
            mode=rospy.get_param('/mode')

        # Get GPS channel if connected.
        gpsChannel="/gps/fix" 
        if (rospy.has_param('/GPSChannel')):
            gpsChannel=rospy.get_param('/GPSChannel')

        # Subscribe to ROS communications & GPS channels.
        comsub = rospy.Subscriber("comms", String, self.comms_callback)
        navsub = rospy.Subscriber(gpsChannel, NavSatFix, self.nav_callback)

        # Innitialise socket protocol from comms.py.
        comms.conman_init(ip, port, TMID)
        self.hbstate = {
            'mode': mode,
            'UAVstat': 1 # UAV is stowed by default.
        }

        
        self.hbready = False # Flag for heartbeat ready.

        # CHeck for debug status in ROS.
        if rospy.has_param('/debug'):

            # Add dummy coords if in debug mode.
            self.hbstate = {
                'latitude': 0,
                'longitude': 0,
                'longEW': 'E',
                'latNS': 'N',
                'mode': mode,
                'UAVstat': 1
            }
            self.hbready = True # Heatbeat is now ready with dummy coords.
            

    def nav_callback(self, msg): # Assigns NS & EW to coords as appropriate.
        
        self.hbstate.latitude = abs(msg.latitude)
        if (msg.latitude>0):
            self.hbstate.latNS='N'
        else:
            self.hbstate.latNS='S'
            
        self.hbstate.longitude = abs(msg.longitude)
        if (msg.longitude>0):
            self.hbstate.longEW='E'
        else:
            self.hbstate.longEW='W'
            
        self.hbready=True # Heatbeat is now ready.
        

    def comms_callback(self, msg): # Probably superfluous?
        """Processes messages from communications.

        Arguments:
            msg {[type]} -- [description]
        """
        pass
    

    def send_heartbeat(self): # Sends the heartbeat.
        """Send the heartbeat message.
        """
        if self.hbready: # CHecks heartbeat is reaqdy to send.
            comms.sendHeartbeatMessage(self.hbstate) # Sends heartbeat.


# This should always be run

conman = _conman() # Init communtiations manager as class.

print("Started Program")
rospy.init_node("communicator") # Create ROS communicator node.

rate = rospy.Rate(1) # Set transmission frequency of 1 Hz.


while not rospy.is_shutdown():

    #print("Inside Loop")
    fakeState = {} # Not sure what this is for ... ?
    conman.send_heartbeat() # Broadcast the heartbeat message

    rate.sleep() # Wait for 1 seccond.
    
