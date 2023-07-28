#COSC473 Introduction to Computer Systems
#Assignment 2
#PART 3 SENDER
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
finish = "F"

P1 = "1"
P2 = "0"
D1 = "1"
P3 = "0"
D2 = "1"
D3 = "0"
D4 = "1"

i = 0

while True:
    if button_a.was_pressed():
        if i == 0:
            body = D4 + D3 + D2 + P3 + D1 + P2 + P1
        elif i == 1:
            body = "0010101"
        elif i == 2:
            body = "1110101"
        elif i == 3:
            body = "1000101"
        elif i == 4:
            body = "1011101"
        elif i == 5:
            body = "1010001"
        elif i == 6:
            body = "1010111"
        elif i == 7:
            body = "1010100"
        message = header + start + body + finish
        radio.send(message)
        
    if button_b.was_pressed():
        i += 1
        i %= 8
        display.scroll(i, delay=80)
#----------------------------------------