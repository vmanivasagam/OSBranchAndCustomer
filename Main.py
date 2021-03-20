import json
import subprocess
import time


# Given a Json with a set of objects containing branches and customers
# count the number of branches and add them to the starting port number to get the last port number
# Given 50051 as startport and 3 branches, the lastPortNumber will be 50054, however really the port numbers assigned to the process will be 50051, 50052 and 50053
def identifyLastPort(jsonObjs, startport):
    lastPortNumber=startport
    for obj in jsonObjs:
        if("branch"==obj["type"]):
            lastPortNumber=lastPortNumber+1
    return lastPortNumber



# Read the Input file
f=open("Input.txt", "r")
ip=json.loads(f.read())

# Assume the starting port numbers for the branches and customers
branchport=50051
customerport=50051

# Identify the last port number based on the number of branch objects
lastPortNumber=identifyLastPort(ip, branchport)

#Loop through the objects in the input file creating branches first
for obj in ip:
    if("branch"==obj["type"]):
        p1=subprocess.Popen('python Branch.py ' + str(branchport)+" "+ str(obj["id"])+" \""+ str(obj["balance"]) + "\" "+ str(lastPortNumber))
        print("Main.py - Branch process started at port" + str(branchport))
        #print(p1)
        branchport=branchport+1

time.sleep(3)
for obj in ip: 
    if("customer"==obj["type"]):
        #print("RRRRRRRRRRRR", obj["events"])
        #print(json.dumps(obj["events"]))
        p1=subprocess.Popen('python Customer.py ' + str(customerport) +" "+ str(obj["id"])+" \""+ str(obj["events"]) + "\"")
        print("Main.py - Customer process started at port" + str(customerport))
        #print(p1)
        customerport=customerport+1

