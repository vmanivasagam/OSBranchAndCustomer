import grpc
import example_pb2
import example_pb2_grpc
import time
import sys
import json

class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.channel=grpc.insecure_channel('localhost:'+ str(thisport))
        # stub for calling the server process
        self.stub = self.createStub()
        # This is the string to construct the output process
        self.output='{"id": '+self.id+ ', "recv": ['


    # TODO: students are expected to create the Customer stub
    # Response: Created the customer stub
    def createStub(self):
        return example_pb2_grpc.RPCStub(self.channel)

    # TODO: students are expected to send out the events to the Bank
    # Response: Created an iterator for the events and sending the events to branch
    def executeEvents(self):
        # when sent over command line args, the double quote changes to single quote and hence not parsable as a json. 
        # So need to convert it back
        self.events=self.events.replace("\'", "\"")

        # Loop over all events
        for event in json.loads(self.events):
            # Call the MsgDeliveryRequest for each of the events
            response = self.stub.MsgDelivery(example_pb2.MsgDeliveryRequest(id=event["id"], money=event["money"], dest=event["id"], interface=event["interface"]))
            print(printableCustomer," - Response: ",response)

            # Format the output string based on the event type
            if("query"==event["interface"]):
                self.output=self.output+ '{"interface": "'+ response.interface+'", "result": "'+ response.result+'", "money": '+str(response.money)+'}, ' 
            else:
                self.output=self.output+ '{"interface": "'+ response.interface+'", "result": "'+ response.result+'"}, ' 
        
        # Finishing touches for the output string        
        self.output=self.output[:-2]+']}'
        return self.output

# Command Line Args passed to this process
#   1st Arg = The port number for the current customer process
#   2nd Arg = The ID of the customer
#   3rd Arg = The events associated with the customer
if __name__ == '__main__':
    
    thisport=sys.argv[1]
    customerid=sys.argv[2]
    customerevents=sys.argv[3]


    # Print statements for denoting start of Customer process
    printableCustomer="Customer@"+thisport
    print(printableCustomer, " - Main: ", "Customer process started at port: ", thisport, "with ID: ", customerid, " and events: ", customerevents)
    
    # Start the customer process
    c=Customer(customerid, customerevents)

    # Execute the events associated with the customer
    op=c.executeEvents()

    # Open the output file for append and add the output string
    f=open("Output.txt", "a")
    f.write(op)
