#!/usr/bin/env python3

import datetime # Gets current date & time.
import socket
import std_msgs
import rospy # Python package for ROS


### GLOBAL VARIABLES

TEAMID = 'DESIG' # Assigned by technical director.
# Also defined in conman.py

s = 0 # Placeholder for stream socket defined in conman_init()


print("Comms Started")
def formatAndSend(header, data, addID=1): # Add header, footer, & checksum to message
    
    print("Inside foramat and send")
    result = "$" + header + "," # Add to start of message

    now = datetime.datetime.now() # Get current time & date.

    # Add current date & time to message.
    result = result+str(now.day)[0:2] + str(now.month)[0:2]+str(now.year)[0:2]+","
    result = result+str(now.hour)[0:2] + str(now.minute)[0:2]+str(now.second)[0:2]+","

    if addID:
        result = result + TEAMID + ","
    
    result = result+data # Add message in the middle.

    # Determine checksum
    checksum = 0
    for i in data:
        checksum = checksum ^ ord(i)
    
    result = result+"*"
    result = result+hex(checksum)[-2:]  # Add checksum to message.
    result = result + '\r\n'
    result_bytes = result.encode() #encoding string to byte for socket.send()

    global s
    try:
        s.send(result_bytes) # Send message.
        print("Message: "+result)
    except Exception:
        print("Message "+result+" not sent!")
   
    return result # Final fomatted message.



def sendHeartbeatMessage(state): # Send the heartbeat message (C3).
    # To be sent at frequency of 1 Hz.
    '''
    state: a dictionary containing:
        latitude: (float)
        latNS: (char) N or S
        longitude: (float)
        longEW: (char) E or W
        mode: (int):
            1: teleop,
            2: auto,
            3: killed
        UAVstat: (int):
            1: Stowed, AUV secured to USV
            2: Deployed
            3: Faulted.
    '''
    
    # Add latitude & longitude.
    message = str(state['latitude'])+","+state['latNS']+","
    message = message+str(state['longitude'])+","+state['longEW']+","

    message = message+TEAMID+"," # Add team ID

    message = message+str(state['mode'])+"," # Add mode.
    # Mode 1 = Remote operated.
    # Mode 2 = Autonomous.
    # Mode 3 = Killed.
    
    message = message+str(state['UAVstat']) # Add UAV status
    # 1: Stowed
    # 2: Deployed
    # 3: Faulted. 
    
    message=formatAndSend("RXHRB", message, 0) # Format message.
    return message



def sendGatesMessage(state): # Send message for enterance & exit gates (C4).
    # To report gate where active beacon detected.
    '''
    state: a dictionary containing:
        active_entrance_gate (int)
        active_exit_gate (int)
    '''
  
    # Add active gates
    message = str(state['active_entrance_gate'])+","
    message = message+str(state["active_exit_gate"])
    
    message = formatAndSend('RXGAT', message) # Format message.
    return message



def sendFollowPathMessage(state): # Send message to signal completion of path. (C5)
    
    '''
    state: a dictionary containing:
        finished (int):
            1: In progress
            2: Completed
    '''
    
    message = state["finished"] # Add light pattern.
    
    message = formatAndSend("RXPTH", message) # Format with checksum
    return message



def sendWildlifeMessage(state): # Send message to signal completion of path. (C6)
    '''
    state: a dictionary containing:
        num_detected (int): 1 to 3
        first_wildlife (char): P or C or T
        seccond_wildlife (char): P or C or T
        third_wildlife (char): P or C or T
    '''
    
    message = state["finished"] # Add light pattern.
    
    message = formatAndSend("RXENC", message) # Format with checksum
    return message


def sendScanCodeMessage(state): # Send message for light tower (C7)

    '''
    state: a dictionary containing:
        lignt_pattern (string): Order of ifentified lights. eg. "RBG"
    '''
    
    message = state["light_pattern"] # Add light pattern.
    
    message = formatAndSend("RXCOD", message) # Format with checksum
    return message


def sendDockMessage(state): # Send message for Detect & Dock (C8)
    '''
    state: a dictionary containing:
        color (char): R or G or B
        ams_status (int):
            1: Docking
            2: Complete
    '''
    
    message = state["color"]+","
    message = message+state["ams_status"]
    
    message = formatAndSend("RXDOK", message)
    return message



def sendFlingMessage(state): # Send message for find and fling (C9).
    '''
    state: a dictionary containing:
        color (char): R or G or B
        fling_status (int):
            1: Scanning
            2: Flinging
    '''
    
    message = state["color"]+","
    message = message+state["fling_status"]
    
    message = formatAndSend("RXFLG", message)
    return message



def sendUAVReplenishmentMessage(state):
    pass


def sendSearchAndReportMessage(state):
    pass



BUFFER_SIZE = 1024 # Possibly Unused?


def conman_init(TCP_IP,TCP_PORT,TID): # Initialise communications manager.
    
    global s
    
    global TEAMID # Access default team ID.
    TEAMID=TID # Allow extermial TEAMID definition.
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create stream socket.
    s.connect((TCP_IP, TCP_PORT)) # Connect socket.


if __name__=='__main__': # Not imported as a module.
    conman_init('0.0.0.0',9999) # Initialise communications manager.
    
