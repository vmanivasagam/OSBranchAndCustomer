import json
import subprocess
import time
import multiprocessing
import os

# Given a Json with a set of objects containing branches and customers
# count the number of branches and add them to the starting port number to get the last port number plus one
# Given 50051 as startport and 3 branches, the lastPortNumber will be 50054, however really the port numbers assigned to the process will be 50051, 50052 and 50053
def identifyLastPortPlusOne(jsonObjs, startport):
    lastPortNumber=startport
    for obj in jsonObjs:
        if("branch"==obj["type"]):
            lastPortNumber=lastPortNumber+1
    return lastPortNumber


# This is the method used to start the branch. 
# Parameters:
#   branchport - The port number at which the branch process has to be started
#   obj - The JSON object containing the branch information
#   lastPortNumberPlusOne - Contains the last port number assigned to the branch plus one.
def startBranch(branchport, obj, lastPortNumberPlusOne):
    return os.system(('python Branch.py ') + str(branchport)+" "+ str(obj["id"])+" \""+ str(obj["balance"]) + "\" "+ str(lastPortNumberPlusOne))



# Main fn
if __name__=="__main__":

    # Read the Input file
    f=open("Input.txt", "r")
    ip=json.loads(f.read())

    # Assume the starting port numbers for the branches and customers
    branchport=50051
    customerport=50051

    # Identify the last port number plus one based on the number of branch objects
    lastPortNumberPlusOne=identifyLastPortPlusOne(ip, branchport)


    '''for obj in ip:
        if("branch"==obj["type"]):
            p1=subprocess.Popen('python Branch.py ' + str(branchport)+" "+ str(obj["id"])+" \""+ str(obj["balance"]) + "\" "+ str(lastPortNumber))
            print("Main.py - Branch process started at port" + str(branchport))
            #print(p1)
            branchport=branchport+1
    '''

    # Loop through the objects in the input file creating branches first    
    # bnch will contain the list of all branch processes created by the multiprocessing.Process fn.
    bnch=[]
    for obj in ip:
        if("branch"==obj["type"]):
            bnch.append(multiprocessing.Process(target=startBranch, args=(branchport, obj, lastPortNumberPlusOne)))
            print("Main.py - Branch process started at port" + str(branchport))
            branchport=branchport+1

    # Now start all the branch processes.
    for b in bnch:
        b.start()

    # This timer is to make sure all the branch process starts before the customer process.
    time.sleep(1)

    # Now create all the customer process using subprocess.Popen
    for obj in ip: 
        if("customer"==obj["type"]):
            p1=subprocess.Popen('python Customer.py ' + str(customerport) +" "+ str(obj["id"])+" \""+ str(obj["events"]) + "\"")
            print("Main.py - Customer process started at port" + str(customerport))
            customerport=customerport+1





'''def startBranch1(num):
    print("startBranchhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    os.system('python Branch.py "50051" "1" "400" "50054"')# + str(branchport)+" "+ str(obj["id"])+" \""+ str(obj["balance"]) + "\" "+ str(lastPortNumber))
def startBranch2(num):
    os.system('python Branch.py "50052" "2" "400" "50054"')
def startBranch3(num):
    os.system('python Branch.py "50053" "3" "400" "50054"')
'''
