#COSC473 Introduction to Computer Systems
#Assignment 2
#PART 3 RECEIVER
#Quoc Tran - s3827826
#----------------------------------------

from microbit import * 
import radio 
import random

radio.on()

sourceID = "MC"

def receiveData():
        messageIndex = received.find("S") + 1
        finishIndex = received.find("F")
        message = received[messageIndex:finishIndex]
        display.scroll(message)
        D4 = int(message[0:1])
        D3 = int(message[1:2])
        D2 = int(message[2:3])
        P3 = int(message[3:4])
        D1 = int(message[4:5])
        P2 = int(message[5:6])
        P1 = int(message[6:])
        return message, P1, P2, P3, D1, D2, D3, D4

while True:
    received = radio.receive()
    if received and received[2:4] == "MC":
        message, P1, P2, P3, D1, D2, D3, D4 = receiveData()
                
        if ((P1 + D1 + D2 + D4) % 2 == 0) and ((P2 + D1 + D3 + D4) % 2 == 0) and ((P3 + D2 + D3 + D4) % 2 == 0):
            display.show(Image.YES)
            sleep(3000)
            display.clear()
        else:
            display.show(Image.NO)
            sleep(3000)
            display.clear()
            
            P1 = (P1 + D1 + D2 + D4) % 2
            P2 = (P2 + D1 + D3 + D4) % 2
            P3 = (P3 + D2 + D3 + D4) % 2
            
            bitPositionOfError = (P3 * 4) + (P2 * 2) + (P1 * 1)
            indexPositionOfError = len(message) - bitPositionOfError
            correctedBit = (int(message[indexPositionOfError]) + 1) % 2

            if indexPositionOfError == 0:
                correctedMessage = str(correctedBit) + message[1:]
            elif indexPositionOfError == len(message):
                correctedMessage = message[0:len(message)] + str(correctedBit)
            else:
                correctedMessage = message[0:indexPositionOfError] + str(correctedBit) + message[indexPositionOfError+1:len(message)]
            display.scroll(correctedMessage)
            display.show(Image.HAPPY)
            sleep(3000)
            display.clear()
#----------------------------------------            