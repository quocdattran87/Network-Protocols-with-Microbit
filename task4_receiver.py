#COSC473 Introduction to Computer Systems
#Assignment 2
#PART 4 RECEIVER
#Quoc Tran - s3827826
#----------------------------------------

from microbit import * 
import radio

radio.on()

sourceIP = "192.168.1.2"
destinationIP = ""
uniqueID = "0x65f402f"
sourceMAC = "BBB"
destinationMAC = ""
operation = "2"

def ARPRequest():
    destinationMAC = received[0:3]
    destinationIP = received[3:6]
    display.scroll(destinationMAC)
    ARPReply = sourceMAC + sourceIP[8:] + destinationIP + operation
    radio.send(ARPReply)
    return destinationMAC, destinationIP
        
def packetReceived():
    if received and sourceMAC in received:
        messageIndex = received.find(sourceIP[8:]) + 3
        message = received[messageIndex:len(received)]
        display.scroll(message)

while True:
    received = radio.receive()
    if received and sourceIP[8:] == received[len(received)-4: len(received) -1]:
        if received[len(received)-1] == "1": #Operation number 1 means an ARP request.
            destinationMAC, destinationIP = ARPRequest()

    packetReceived()
#----------------------------------------            
