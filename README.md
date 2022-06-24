WAMV Communications.
====================

Scripts that govern the WAMV status heartbeat and the transmission of task specific messages for the 2022 RobotX competition.

The status heartbeat is handled entirely by these scripts, and should not need to be interacted with by any other component of the WAMV software. Note that the status heartbeat is that described by appendix C3 of the 2022 competition handbook. *This is entirely different to the 3 LCM heartbeats that are used for process coordination.*

Unlike the heartbeat, the task specific messages exist as python functions in `wamv_comms/scripts/comms.py`. To send these messages, the script responsible for running the task must call the functions from `comms.py` as defined below.

## Functions and parameters required to transmit task specific status messages:


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


**UAV search & report message (C9): `sendSearchAndReportMessage(state)`**

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
