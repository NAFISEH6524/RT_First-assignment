from __future__ import print_function

import time
from sr.robot import *


# Lists that store the silver and golden tokens that have already been paired
silver_list = []
gold_list = []

# Variable for letting the robot know if it has to look for a silver or for a golden token
silverflag = True
gold_threshold = 0.8

# Threshold for the control of the linear distance
a_threshold = 2.0

# Threshold for the control of the orientation
d_threshold = 0.4

# Instance of the class Robot
R = Robot()

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_silver_token():
    """
    Function to find the closest silver token   
    Returns:
    dist (float): distance of the closest token (-1 if no token is detected)
    rot_y (float): angle between the robot and the token (-1 if no token is detected)
    code: identifier of the silver token (-1 if no silver token is detected)
     """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and token.info.code not in silver_list :
            dist = token.dist
            rot_y = token.rot_y
            code = token.info.code
           
    if dist==100:
        return -1, -1, -1
    else:
        return code, dist, rot_y

def find_gold_token():
    """
    Function to find the closest     
    Returns:
    dist (float): distance of the closest token (-1 if no token is detected)
    rot_y (float): angle between the robot and the token (-1 if no token is detected)
    code: identifier of the gold token (-1 if no gold token is detected)
     """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and token.info.code not in gold_list:
            
            dist = token.dist
            rot_y = token.rot_y
            code = token.info.code
    if dist==100:
        return -1, -1, -1
    else:
        return code, dist, rot_y


while len(gold_list) < 6:
   
    if silverflag == True: #if silver is true , then we look for a silver token, otherwise for a golden token
        code , dist_silver , rot_y= find_silver_token()
        print("silver.info")
        if dist_silver==-1:
            print("I don't see any token!!")
            turn(+10, 1)
        elif dist_silver < d_threshold:
            print("Found it!")
            if R.grab():
                silver_list.append(code)
                print("Gotcha!")
                turn(-20, 2)
                silverflag = not silverflag 
            else:
                print("Aww, I'm not close enough!")
        elif -a_threshold <= rot_y <= a_threshold:
            # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            drive(30, 0.5)
        elif rot_y < -a_threshold:
            print("Left a bit ...")
            turn(-2, 0.5)
        elif rot_y > a_threshold:
            print("Right a bit ...")
            turn(+2, 0.5)
    else:
        code , dist_gold , rot_y = find_gold_token()
        print("Gold.info")
        if dist_gold==-1:
            print("I don't see any token!!")
            turn(+10, 1)
        elif dist_gold < d_threshold:
            print("Found it!")
            if R.grab():
                print("Gotcha!")
                turn(-20, 2)
            else:
                print("Aww, I'm not close enough!")
        elif -a_threshold <= rot_y <= a_threshold:
            # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            drive(30, 0.5)
            if dist_gold <= gold_threshold and dist_gold != -1:
                R.release()
                gold_list.append(code)
                drive(-10, 2)
                silverflag = True
                print("")
        elif rot_y < -a_threshold:
            print("Left a bit ...")
            turn(-2, 0.5)
        elif rot_y > a_threshold:
            print("Right a bit ...")
            turn(+2, 0.5)
    