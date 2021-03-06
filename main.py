from systemetric import *
from sr2013 import *
import time
import math

R = PacBot("comp")


def Pick():
    markers = R.see()
    print("Saw {} markers".format(len(markers)))
    arena_list, robot_list, pedestal_list, cube_list = sortMarkers(markers)
    if len(cube_list) == 0:
        print("No cubes seen")
        return False
    print("Seen a cube")
    MovementTarget = markerDistance(cube_list[0])
    R.moveForward(MovementTarget[1])
    if MovementTarget[0] < -0.2:
        R.turn(-90)
        R.moveForward(-MovementTarget[0])
    elif MovementTarget[0] > 0.2:
        R.turn(90)
        R.moveForward(MovementTarget[0])
    pickUpCube()
    return True

def Plinth():
    markers = R.see()
    print("Saw {} markers".format(len(markers)))
    arena_list, robot_list, pedestal_list, cube_list = sortMarkers(markers)
    if len(pedestal_list) == 0:
        print("No pedestals seen")
        return False
    print("Seen a pedestal")
    PlinthTarget = markerDistance(pedestal_list[0])
    AdjustedMovement = (PlinthTarget[0]-MovementTarget[0], PlinthTarget[1]-MovementTarget[1])
    R.moveForward(AdjustedMovement[1])
    if AdjustedMovement[0]*AdjustedMovement[1] < 0:
        R.turn(-90)
        R.moveForward(AdjustedMovement[0])
    elif AdjustedMovement[0]*AdjustedMovement[1] > 0:
        R.turn(90)
        R.moveForward(AdjustedMovement[0])
    dropCube()
    return True
    
def markerDistance(marker):
    """Finds the relative forwards and sideways distance to a marker
    Input: marker
    Output: sideDist, forwardDist, totalDist"""
    forwardDist = 0
    sideDist = 0
    totalDist = 0
    p = marker.centre
    forwardDist = math.sin(math.radians(p.polar.rot_x))*p.polar.length
    sideDist = math.cos(math.radians(p.polar.rot_x))*p.polar.length
    totalDist = sideDist+forwardDist
    return sideDist, forwardDist, totalDist

def sortMarkers(markerList):
    """appends all the marker types to their own list
    input: markerList
    output: arena_list, robot_list, pedestal_list, cube_list"""
    arena_list = []
    robot_list = []
    pedestal_list = []
    cubes_list = []
    for marker in markerList:
        marker.sideDist, marker.forwardDist, marker.totalDist = markerDistance(marker)
        if marker.info.marker_type == MARKER_ARENA:
            arena_list.append(marker)
        if marker.info.marker_type == MARKER_ROBOT:
            robot_list.append(marker)
        if marker.info.marker_type == MARKER_PEDESTAL:
            pedestal_list.append(marker)
        if marker.info.marker_type == MARKER_TOKEN:
            cubes_list.append(marker)
    return arena_list, robot_list, pedestal_list, cubes_list
    
def pickUpCube():
    """Moves the arm down to the cube and sucks up the cube then raises the arm"""
    R.setArmState(1)
    R.setPumpState(True)
    R.setArmState(0)
def dropCube():
    """Releases cube"""
    R.setPumpState(False)

while not Pick(): pass
while not Plinth(): pass
