#COSC473 Introduction to Computer Systems
#Assignment 2
#PART 1 SENDER
#Quoc Tran - s3827826
#----------------------------------------

from microbit import * 
import radio 
import random

radio.on()

sourceID = "QT"
destinationID = "MC"
header = sourceID + destinationID
start = "S"
data = "1"
finish = "F"
sequenceNumber = "0"
goodConnection = "GOOD"
mediumConnection = "MEDIUM"
badConnection = "BAD"
noConnection = "NO"

imageMEH = Image('00000:09090:00000:99999:00000')

framesToSend = 5
errorRating = 0

dataFramesSent = 0
dataFramesReceived = 0
ackFramesSent = 0
ackFramesReceived = 0
x = 0
y = 0

def sendWithError(message, error): 
    generated = random.randint(1, 100) 
    if generated > error:
        radio.send(message)
        
def receiveACK():
    if received and received[2:4] == "QT":
        bodyIndex = received.find("S") + 1
        finishIndex = received.find("F")
        sequenceIndex = finishIndex + 1
        receivedBody = received[bodyIndex:finishIndex]
        ackSequenceNumber = int(received[sequenceIndex:])
        if receivedBody == "ACK" and ackSequenceNumber == int(sequenceNumber):
            return True
        return False

def errorCalculations():
    dataFramesLost = dataFramesSent - dataFramesReceived
    ackFramesLost = ackFramesSent - ackFramesReceived
    failedTransmissions = dataFramesLost + ackFramesLost
    totalTraversedFrames = dataFramesSent + ackFramesSent
    frameLossError = int((failedTransmissions/totalTraversedFrames)*100)
    totalTransmission = ackFramesReceived + failedTransmissions
    failRate = int((failedTransmissions/ totalTransmission)*100)
    return frameLossError, failRate
        
def frameLossReport():
    frameLossError, failRate = errorCalculations()
    if frameLossError >= 80:
        dataFrame = header + start + badConnection + finish + sequenceNumber
        radio.send(dataFrame)
        display.show(Image.SAD)
        sleep(3000)
        display.clear()
    elif frameLossError >= 21 and frameLossError <= 79: 
        dataFrame = header + start + mediumConnection + finish + sequenceNumber
        radio.send(dataFrame)
        display.show(imageMEH)
        sleep(3000)
        display.clear()
    elif frameLossError >= 0 and frameLossError <= 20:
        dataFrame = header + start + goodConnection + finish + sequenceNumber
        radio.send(dataFrame)
        display.show(Image.HAPPY)
        sleep(3000)
        display.clear()
        
def failRate():
    frameLossError, failRate = errorCalculations()
    if failRate >= 90:
        return True
        
def adjustLights():
    global x
    global y
    if x == 4:
        x = -1
        y += 1
    x += 1
        
def reset():
    global dataFramesSent
    global dataFramesReceived
    global ackFramesSent
    global ackFramesReceived
    global x
    global y
    global data
    global sequenceNumber
    dataFramesSent = 0
    dataFramesReceived = 0
    ackFramesSent = 0
    ackFramesReceived = 0
    x = 0
    y = 0
    data = "1"
    sequenceNumber = "0"

while True:
    if button_a.was_pressed():
        while ackFramesReceived < framesToSend:
            #Error check starts at 10 frames sent. 
            #Terminate if 90% fail rate or more than 25 frames sent. ie, the amount of pixels on microbit.
            if (dataFramesSent >= 10 and failRate()) or (dataFramesSent == 25):
                dataFrame = header + start + noConnection + finish + sequenceNumber
                radio.send(dataFrame)
                display.show(Image.NO)
                sleep(3000)
                display.clear()
                break
            
            dataFrame = header + start + data + finish + sequenceNumber
            sendWithError(dataFrame, errorRating) #dataFrame sent
            dataFramesSent += 1
            display.set_pixel(x,y,2) #Data sent light is displayed.
            sleep(2600)
                
            received = radio.receive()
            if receiveACK(): #Correct ACK and Sequence number received.
                ackFramesReceived += 1
                display.set_pixel(x,y,9) #Ack received light is displayed. 
                sleep(1000)
                data = str(int(data) + 1) #Prepare the next data and sequence number for sending.
                sequenceNumber = str(int(sequenceNumber) + 1)
            else:
                #dataFrame fail OR ack fail.
                display.set_pixel(x,y,5) #Time out light is displayed.
                sleep(1000)
                    
            #Get the count for ackFramesSent and dataFramesReceived from the receiver.
            received = radio.receive()
            if received and not receiveACK():
                finishIndex = received.find("F")
                dataFramesReceived = int(received[4:finishIndex])
                ackFramesSent = int(received[finishIndex+1:])
                
            adjustLights() 
            
        frameLossReport()
        reset()
            
    if button_b.was_pressed():
        errorRating += 20
        errorRating %= 120
        display.scroll(errorRating, delay=80)
        
    if accelerometer.was_gesture("shake"):
        framesToSend += 5
        framesToSend %= 30
        if framesToSend == 0:
            framesToSend = 5
        display.scroll(framesToSend, delay=80)
#----------------------------------------