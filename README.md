WAMV Communications.
====================

Scripts that govern the WAMV status heartbeat and the transmission of task specific messages for the 2022 RobotX competition.

The status heartbeat is handled entirely by these scripts, and should not need to be interacted with by any other component of the WAMV software. Note that the status heartbeat is that described by appendix C3 of the 2022 competition handbook. *This is entirely different to the 3 LCM heartbeats that are used for process coordination.*


## Configuring heartbeat parameters: Port, team ID, and IP address.

The status heartbeat is managed by the `conman.py` script, which imports `comms.py` as a module. Ths script requires the following parameters to be defined. By default, these are defined with dummy values in `robotx2022/robotx_ws/src/wamv_comms/launch/commclient.launch`. 

```
<launch>
<param name="ip" value="localhost"/>
<param name="port" value="2000"/>
<param name="TID" value="USYD_ROWBOT"/>
<param name="debug" value="true"/>
<node pkg="wamv_comms" type="conman.py" name="communicator" output="screen"/>
</launch>
```

The heartbeat script will transmit the heartbeat message to the defined IP and port using the Python Socket module.

Section C1 of the 2022 competition handbook states that:
> During operation, teams are provided with a hard wired connection (RJ-45) to the Technical Director's network. This connection must be used to transmit the AMS heartbeat and other reports.
> When connected to the Technical Director network, the team’s computer must request an IP address from a Technical Director Network DHCP server. Once connected, they should establish a TCP connection to a server with an address and port number, correlating to the selected course. Address and port numbers for each course will be provided during the event. 

***At present, this heartbeat script will transmit the heartbeat as a TCP message to a device that is connected to the same network as the WAMV, or te the WAMV's own wireless notwork (untested).** This program does not handle the process of requesting an IP address from the DHCP server, or of transferring the message from via a hard wired connection from the base station over the Technical Director's network.*


## Launching the heartbeat using ROS within a Docker container:

The status heartbeat is setup as a ROS node within the `robotx_ws` catkin workspace. The following steps describe how to directly launch the status  heartbeat.

**Step 1:** Connect to the WAMV via ssh, and start the `robotx_ros` Docker container uning the method described in the operating instructions document (on Trello).

**Step 2:** Navigate to the workspace folder using `cd robotx2022/robotx_ws/`.

**Step 3:** Run `source devel/setup.bash`.

**Step 4:** Launch the status heartbeat ROS node using `roslaunch wamv_comms commclient.launch`. Below is an example of the output given by launching the ROS node, using dummy values for the port and IP, and with the GPS disconnected.

```
root@wamv:/robotx2022/robotx_ws# roslaunch wamv_comms commclient.launch 
... logging to /root/.ros/log/dd79eb12-f742-11ec-b131-0030641daa10/roslaunch-wamv-937.log
Checking log directory for disk usage. This may take a while.
Press Ctrl-C to interrupt
Done checking log file disk usage. Usage is <1GB.

started roslaunch server http://wamv:46417/

SUMMARY
========

PARAMETERS
 * /TID: USYD_ROWBOT
 * /debug: True
 * /ip: localhost
 * /port: 2000
 * /rosdistro: noetic
 * /rosversion: 1.15.14

NODES
  /
    communicator (wamv_comms/conman.py)

ROS_MASTER_URI=http://localhost:11311

process[communicator-1]: started with pid [945]
conman started

Sent message: $RXHRB,29620,1384,0,N,0,E,USYD_ROWBOT,3,1*5e
Sent message: $RXHRB,29620,1385,0,N,0,E,USYD_ROWBOT,3,1*5e
Sent message: $RXHRB,29620,1386,0,N,0,E,USYD_ROWBOT,3,1*5e
Sent message: $RXHRB,29620,1387,0,N,0,E,USYD_ROWBOT,3,1*5e
...
```

## Functions and parameters required to transmit task specific status messages:

Unlike the heartbeat, the task specific messages exist as python functions in `wamv_comms/scripts/comms.py`. To send these messages, the script responsible for running the task must call the functions from `comms.py` as defined below.

**Enterance & exit gates message (C4): `sendGatesMessage(state)`**

```
state: a dictionary containing:
    active_entrance_gate (int) 1 to 3
    active_exit_gate (int) 1 to 3
```

**Follow the path message (C5): `sendFollowPathMessage(state)`**

```
state: a dictionary containing:
    finished (int):
        1: In progress
        2: Completed
```


**Wildlife encounter - react & report message (C6): `sendWildlifeMessage(state)`**

```
state: a dictionary containing:
    num_detected (int): 1 to 3
    first_wildlife (char): P or C or T
    seccond_wildlife (char): P or C or T
    third_wildlife (char): P or C or T
```


**Scan the code message (C7): `sendScanCodeMessage(state)`**

```
state: a dictionary containing:
    lignt_pattern (string): Order of ifentified lights. eg. "RBG"
```


**Detect & dock message (C8): `sendDockMessage(state)`**

```
state: a dictionary containing:
    color (char): R or G or B
    ams_status (int):
        1: Docking
        2: Complete
```

**Find & fling message (C9): `sendFlingMessage(state)`**

```
state: a dictionary containing:
    color (char): R or G or B
    fling_status (int):
        1: Scanning
        2: Flinging
```


**UAV replenishment message (C9): `sendUAVReplenishmentMessage(state)`**

*Not yet implemented.*


**UAV search & report message (C10): `sendSearchAndReportMessage(state)`**

*Not yet implemented.*


**Status heartbeat message (C3): `sendHeartbeatMessage(state)`**

```
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
```

*Note, this is automatically sent at a frequency of 1Hz, and should not be manually called. The following exists only for reference of those who may need to modify the data that is sent*

***For more information, see the transmission specifications described in the 2022 competition handbook.***
