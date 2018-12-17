##############################################
# Kris Bliss
# bliss132@umn.edu
###############################################

##################################################
### Client Program
##################################################
import socket
import sys
import time


NAME = str(sys.argv[1])
HOST = str(sys.argv[2]) # USE '127.0.0.2' 
PORT = int(sys.argv[3]) # USE 5352

# Socket Object for Clinet
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.connect((HOST,PORT))


# Function to take user input
def userInput():
    message = input("What Domain Name are you looking for? \n")
    return message

##################################################
### Parsing and Processing data from Server
##################################################
def messageProcess (message):
    x = 0
    while x < len(message):
        message = message.strip('b') # remove the letter 'b' from client message
        message = message.strip("'") # remove " ' " from the string from client message
        message = message.strip('"')
        message = message.strip('\\')
        x += 1
    return message

##################################################
# Handeling Replys for user readability
#################################################
def dataProcessing(data):
    if data[0] == '0x00':
        print ("\nResponse from:", data[1],'\nIP address is: ',data[2])
    
    elif data[0] == '0x01':
        print ('Could not find IP on default server')
        print ("\n Here is where you may find the IP:", data[1],'\n',data[2])

    elif data[0] == '0xFF' or '0xEE':
        #set size of array for printing
        l = len(data)
        print ("\n Error: ", str(data[l-3]) + ' ' + str(data[-2]) + ' ' + str(data[l-1]) )
    
    


##################################################
### Message and connection handeling for client
#################################################

message = userInput()
while message != '':

    if message != 'q':
        message = str(NAME) +' '+ str(message).lower()
        s.send(str.encode(str(message)))

    # if program is quiting
    else:
        try:
            s.send(str.encode(str(message)))
            print('Closing Connection with server')
        except:
            print('ERROR! Could not Close connection')
        break

    # Pausing program to allow data time to be recived and proccessed
    print("Waiting for response...")

    # recive and print data reply from server
    time.sleep(2)
    response = s.recv(2048)
    response = messageProcess (str(response))
    data = response.split()
    dataProcessing(data)

    # Restart loop
    message = userInput()
    time.sleep(3)