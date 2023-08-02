## First Year University Assignment
By Quoc Tran (s3827826)

This requires two Microbits. One acts as the sender and the other as the receiver. For each protocol, you would upload the code into the respective microbit to see it act out the behaviour.

## Report
### Task 1 (Basic System): Stop and Wait with ARQ
The design of my basic system imitates that of a simple stop and wait protocol with ARQ implemented to recover from lost frames. The sending microbit sends a data frame and a timer starts that waits for acknowledgement from the receiver. If it doesn’t receive the acknowledgement before the timer runs out, it resends the same data frame. If it does receive acknowledgement it then sends the next data frame.

If an acknowledgement is lost, the sender resends the same frame after the time out. If the data is lost, the receiver does not send an ack at all, and the time will run out as well, so the sender will still send the same data frame.

The full form of my data frame is: Header + Start + Data + Finish + sequenceNumber.

Here is a break down of each part of the data frame:

Header = sourceID + destinationID, where each ID is a two-string initial.
Start = “S” to signify the start of the data section.
Finish = “F” to signify the end of the data section.
Data = “1” which is the actual data the sender wants to send. I chose a consecutive number of integers as I felt it was easier to keep track of and debug. This data sits in between the “S” and “F” so it is easier to find the index of the data.
Sequence Number = 0. This increments as each successful acknowledgement is received.



### Task 2 (Improved System): Stop and Wait with ARQ and Sliding Window
For the improved system, I used the basic system as the foundation and tried to build upon it. The main difference is the sender now sends multiple data frames straight away. The amount of frames it sends is dependent on the window size.  For example, if the window size was three, the sender would send three data frames straight away to the receiver. Once it receives an acknowledgement for the first frame, it then sends the fourth data frame. Once it receives acknowledgment for the second frame, it sends the fifth data frame. If it doesn’t receive the next acknowledgement before the time out period, it resend all three frames that is currently in the window.

The data frame design and functions used are very similar to part 1. The most important part for this to work is to be able to keep track of the sequence number so that the receiver knew to send the correct acknowledgement for the correct data in case one is lost or corrupt. To manage the window size, I used a while loop on an index variable to check that it was below the given window size to make sure the correct amount of data was sent at any time.

### Task 3: Error detection
In deciding on how to demonstrate an error detection process, I went with a 7-bit message with even parity. On the sender microbit, you can send a predetermined 7-bit message that is correct by pressing A. When you press B, it creates an error in just the 7th bit position, pressing B again creates a message with an error in just the 6th bit position and so on. Pressing A will send whatever message you are currently on. So, the sender just cycles through one message and its different single bit errors. The receiver stays idle until a message is received. When a message is received, it will break it up and put each bit into variables labelled P1, P2, D1, P3, D2, D3, D4. 

It performs parity checks for each parity grouping and returns True if they all pass, i.e. they are all even parity. The message is scrolled on the screen and the microbit returns to its idle stage. If a parity check fails, all the parity groups are added and have mod2 applied to them. So, if any parity group is in error, that parity group has a result of 1. This is then used to create a binary representation as P3, P2, P1 and converted into decimal. This is the bit location of the error. So, if you minus this from the length of the message, you get the string position of the error. Adding 1 to the error position and mod2 will correct it. Put the string back together and scroll it across the screen for the user to read. The receiver microbit then returns to its idle state awaiting another message.


### Task 4: Address Resolution Protocol (ARP)
They way I attempted to implement an ARP system seems very similar to the data frames sender and receiver ID checks. I am sure this is not quite the same as ARP but when I watched online videos, it seemed like a similar process but instead of ID checks, IP addresses and MAC addresses are used instead. So in trying to implement this logic, I had one microbit send a broadcast with a target IP. The microbit with that IP receives it and sends it’s unique microbit code back. The first microbit then displays this unique code on the screen to show it receieved the code. Using this unique code is no sends a “Hi!” message back.

The data packet formation is as follows: Destination MAC + Source MAC + Destination IP + Source IP + Message

I opted to go for custom MAC address and shortened the IP address to the last three digits as there seemed to be a limit on the length of strings that a microbit can send and some were getting cut short. It took me a while to figure why this was happening. I left the unique microbit IDs in the code because I thought they were cool to have in there. 

I attempted to implement the logic of an ARP process without the use of tables as I was unsure how to code a table in. Instead I used empty variables and “if” logic to see if they held a value. The sender presses A to send a message to the destination MAC address. But first it checks to see if it has the destination MAC stored. If it doesn’t it instead sends an ARP reply to the receiver microbit using it’s IP address and an operation number “1” to indicate a request. 

The ARP request and packet is as follows: Source MAC + Source IP + Destination IP + Operation

The receiver microbit receives this packet and deciphers it to be an ARP request by checking the operation number. It then sends an ARP reply using the same format except it uses it’s source MAC, source IP, the destination IP that it worked out from the ARP request and changes the operation number to “2” to indicate a reply. It also stores the MAC and IP of the senders into variables that it can later access. The sender microbit receives the reply and stores it’s MAC address in a variable. The next time A is pressed it sends a direct message to the receiver microbit.

The concept of ARP tables came up in my readings but I didn’t manage to figure out how to make a table in python. I thought I mimicked the logic of an ARP request and reply pretty decently using the tools that I did know. The main limitations in this program is that everything is hardcoded to receive specific packet sizes with each segment being the same. If an IP address or MAC address was a different length then the program wouldn’t work. Also each microbit can only keep one MAC address in its variable, and the IP information is kept separately from the MAC address, as opposed to being filed together in an ARP table among other entries.
