import grpc
import example_pb2
import example_pb2_grpc
from concurrent import futures
import sys
import time
import json


class Branch(example_pb2_grpc.RPCServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches

        # TODO: students are expected to store the processID of the branches
        # Response: Yes, it is stored as part of the last Branch port args
        pass

    # TODO: students are expected to process requests from both Client and Branch
    # Response: Yes, this method process requests from both Client and Branches
    def MsgDelivery(self,request, context):
        interface=request.interface
        if("query"==interface): # Query process from Customer
            time.sleep(3)
            return self.Query(request, context)
        elif("deposit"==interface): # Deposit process from Customer
            return self.Deposit(request, context)
        elif("withdraw"==interface): # Withdraw process from Customer
            return self.Withdraw(request, context)
        elif("propagate-withdraw"==interface): # Propagate-Withdraw process from Branch
            self.balance=int(self.balance) - request.money
            print(printableBranch, " - Balance Propagation", self.balance)
            return self.Query(request, context)
        elif("propagate-deposit"==interface): # Propagate-Deposit process from Branch
            self.balance=int(self.balance) + request.money
            print(printableBranch, " - Balance Propagation", self.balance)
            return self.Query(request, context)

    # Query process
    # Returns the branch balance
    def Query(self, request, context):
        self.balance=int(self.balance)
        print(printableBranch, " - QUERY, Updated Balance:", self.balance)
        return example_pb2.MsgDeliveryReply(id=request.id, money=int(self.balance), result="success", interface=request.interface)

    # Deposit process
    # Returns the balance post the deposit process and will also propagate the balance to all the branches
    def Deposit(self, request, context):
        self.balance=int(self.balance) + request.money
        print(printableBranch, " - DEPOSIT, Updated Balance:", self.balance)
        self.Propogate_Deposit(request.money)
        return example_pb2.MsgDeliveryReply(id=request.id, money=self.balance, result="success", interface=request.interface)

    # Withdraw process
    # Returns the balance post the withdraw process and will also propagate the balance to all the branches.
    def Withdraw(self, request, context):
        print(int(self.balance), request.money)
        if(int(self.balance) > request.money):
            self.balance=int(self.balance) - request.money
            print(printableBranch, "- WITHDRAW, Updated Balance:", self.balance)
            self.Propogate_Withdraw(request.money)
            return example_pb2.MsgDeliveryReply(id=request.id, money=self.balance, result="success", interface=request.interface)
        else:
            self.balance=int(self.balance)
            print(printableBranch, "- WITHDRAW, Updated Balance:", self.balance)
            self.Propogate_Withdraw(0)
            return example_pb2.MsgDeliveryReply(id=request.id, money=self.balance, result="failure", interface=request.interface)


    # Propagate the Withdraw process
    # Takes in the balance and propagates the balance to all the branches from the starting port number to the last branch port
    def Propogate_Withdraw(self, amount):
        print(printableBranch, "- PROPAGATE WITHDRAW")
        for port in range(50051, int(lastBranchPortPlusOne)):
            if(int(thisport)!=port):
                ch=grpc.insecure_channel('localhost:'+ str(port))
                st=example_pb2_grpc.RPCStub(ch)
                rsp = st.MsgDelivery(example_pb2.MsgDeliveryRequest(id=1, money=amount, dest=1, interface="propagate-withdraw"))

    # Propagate the Deposit process
    # Takes in the balance and propagates the balance to all the branches from the starting port number to the last branch port
    def Propogate_Deposit(self, amount):
        print(printableBranch, "- PROPAGATE DEPOSIT")
        for port in range(50051, int(lastBranchPortPlusOne)):
            if(int(thisport)!=port):
                ch=grpc.insecure_channel('localhost:'+ str(port))
                st=example_pb2_grpc.RPCStub(ch)
                rsp = st.MsgDelivery(example_pb2.MsgDeliveryRequest(id=1, money=amount, dest=1, interface="propagate-deposit"))

# Command Line Args passed to this process
#   1st Arg = The port number for the current branch process
#   2nd Arg = The ID of the branch
#   3rd Arg = The starting balance of the branch
#   4th Arg = The last branch's port number plus one - Used to propagate the balance.
if __name__ == '__main__':
    # grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Read the command line args
    thisport=sys.argv[1]
    branchid=sys.argv[2]
    branchbalance=sys.argv[3]
    lastBranchPortPlusOne=sys.argv[4]

    # Few print statements required to identify the start of the branch process
    printableBranch ="Branch@"+thisport
    print(printableBranch, " - Main: ", "Branch process started at port: ", thisport, "with ID: ", branchid, ", balance: ", branchbalance, " and LastBranchPort", lastBranchPortPlusOne)

    # Create the Branch server process with the ID and the balance
    example_pb2_grpc.add_RPCServicer_to_server(Branch(branchid,branchbalance,1), server)
    server.add_insecure_port('[::]:'+thisport)
    server.start()
    #server.wait_for_termination()
    time.sleep(5)
    exit()