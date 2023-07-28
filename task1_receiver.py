#COSC473 Introduction to Computer Systems
#Assignment 2
#PART 1 RECEIVER
#Quoc Tran - s3827826
#----------------------------------------

from microbit import * 
import radio
import random

radio.on()

sourceID = "MC"
destinationID = "QT"
header = sourceID + destinationID
start = "S"
body = "ACK"
finish = "F"
sequenceNumber = "0"

errorRating = 0

dataFramesReceived = 0
ackFramesSent = 0

image1 = Image('00000:00000:00900:00000:00000')
image2 = Image('00000:00000:09990:00000:00000')
image3 = Image('00000:00900:00900:00900:00000')
imageMEH = Image('00000:09090:00000:99999:00000')

def sendWithError(message, error): 
    generated = random.randint(1, 100) 
    if generated > error:
        radio.send(message)
        ackSendAnimation()
        return True
    else:
        ackFailAnimation()
        return False
    
def receiveData():
    if received and received[2:4] == "MC":
        bodyIndex = received.find("S") + 1
        finishIndex = received.find("F")
        sequenceIndex = finishIndex + 1
        receivedBody = received[bodyIndex:finishIndex]
        dataSequenceNumber = int(received[sequenceIndex:])
        dataSequenceCheck = int(sequenceNumber)
        if receivedBody == "GOOD":
            display.show(Image.HAPPY)
            sleep(3000)
            display.clear()
            reset()
            return False
        elif receivedBody == "MEDIUM":
            display.show(imageMEH)
            sleep(3000)
            display.clear()
            reset()
            return False
        elif receivedBody == "BAD":
            display.show(Image.SAD)
            sleep(3000)
            display.clear()
            reset()
            return False
        elif receivedBody == "NO":
            display.show(Image.NO)
            sleep(3000)
            display.clear()
            return False
        elif receivedBody.isdigit() and dataSequenceCheck == dataSequenceNumber:
            display.scroll(receivedBody, delay=90)
            return True
    
def ackSendAnimation():
    i = 0
    for i in range(5):
        display.set_pixel(i,2,9)
        sleep(150)
    display.clear()

def ackFailAnimation():
    display.show(image1)
    sleep(150)
    display.show(image2)
    sleep(150)
    display.show(image1)
    sleep(150)
    display.show(image3)
    sleep(150)
    display.clear()
    
def reset():
    global dataFramesReceived
    global ackFramesSent
    global sequenceNumber
    dataFramesReceived = 0
    ackFramesSent = 0
    sequenceNumber = "0"
    
while True:
    received = radio.receive()
    if receiveData():
        dataFramesReceived += 1
        ackFrame = header + start + body + finish + sequenceNumber
        if sendWithError(ackFrame, errorRating): #Send ackFrame.
            sequenceNumber = str(int(sequenceNumber) + 1) #Adjust ack sequence number.
        else:
            radio.send("Ghost Signal") #If error, send a signal to capture the first receieve function in the sender file.
        
        ackFramesSent += 1
        #Send dataFramesReceived and ackFramesSent with no error for error calculations.   
        radio.send(header + str(int(dataFramesReceived)) + finish + str(int(ackFramesSent)))

    if button_b.was_pressed():
        errorRating += 20
        errorRating %= 120
        display.scroll(errorRating, delay=80)
#----------------------------------------