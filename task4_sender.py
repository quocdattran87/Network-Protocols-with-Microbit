#COSC473 Introduction to Computer Systems
#Assignment 2
#PART 4 SENDER
#Quoc Tran - s3827826
#----------------------------------------

from microbit import *
import radio

radio.on()

sourceIP = "192.168.1.1"
destinationIP = "192.168.1.2"
uniqueID = "-0x1bdde2fa"
sourceMAC = "AAA"
destinationMAC = ""
operation = "1"

message = "Hi!"
IPPacket = sourceIP[8:] + destinationIP[8:] + message

while True:
    received = radio.receive()
    if received and sourceIP[8:] == received[len(received)-4: len(received)-1]: #IP is addressed to sender microbit.
        if received[len(received)-1] == "2": #Operation number is 2, meaning an ARP reply.
            destinationMAC = received[0:3]
            display.scroll(destinationMAC)

    if button_a.was_pressed():
        if destinationMAC and destinationIP:
            frame = destinationMAC + sourceMAC + IPPacket
            radio.send(frame)
            display.show(Image.HAPPY)
            sleep(3000)
            display.clear()
        else:
            ARPRequest = sourceMAC + sourceIP[8:] + destinationIP[8:] + operation
            radio.send(ARPRequest)
#----------------------------------------
