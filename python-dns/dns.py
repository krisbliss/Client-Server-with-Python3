##############################################
# Kris Bliss
# bliss132@umn.edu
###############################################

###############################################
### DNS program 
###############################################
import socketserver
import socket
import sys
import time
from _thread import *
from collections import defaultdict

# test print
print ("CMD inputs: ", str(sys.argv)) #system arguments for setting server type


##################################################
### Setting the type of server
##################################################

server_dic = {
    'default': ['127.0.0.2',5352],
    'root': ['127.0.0.3',5353],
    'org': ['127.0.0.4',5354],
    'gov': ['127.0.0.5',5355],
    'com': ['127.0.0.6',5356]
}

#init host and port variables
HOST = ''
PORT = 0
NAME = ''

for name in server_dic:
    if (sys.argv[1] == name):
        # Tells user the name of server they have created
        NAME = name
        print ('Server name: ', NAME)
        #Tells user what Host ip is of server
        HOST = server_dic[name][0]
        print ('Host: ', HOST)
        # Tells user what Port Server is usin
        PORT = server_dic[name][1]
        print ('Port: ', PORT)

##################################################
### Create log file
##################################################
def createLogFile(name,message):

    # Create log file
    fileName = '%s.log' % name
    time.sleep(1)
    f = open(fileName, 'a+')
    f.write(str(message)+'\n')
    print ('Logged: ', message)

##################################################
### For com, org, and gov servers to handle data
##################################################
def openFileName(name):

    # Open and read .dat files
    fileName = '%s.dat' % name
    f = open(fileName, 'r')
    print ('Opening File: ', fileName)
    data = f.read()
    data = data.split()
    print(data)

    return data

if NAME == 'root':
    dns_data = openFileName('server')

elif NAME == "com":
    dns_data = openFileName('com')

elif NAME == "gov":
    dns_data = openFileName('gov')

elif NAME == 'org':
    dns_data = openFileName('org')
    

##################################################
### Parsing and Processing data from Client
##################################################
def messageProcess (message):
    x = 0
    while x < len(message):
        message = message.strip('b') # remove the letter 'b' from client message
        message = message.strip("'") # remove " ' " from the string from client message
        message = message.strip('"')
        x += 1
    return message


##################################################
### Create socket and open ports
##################################################
    # SOCEKT_STREAM = TCP protocol 
    # AF_INET = IPv4
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(10) 
print ("Listening on port ", PORT)

##################################################
### Closing Connection function
##################################################
def closeConnection():
    try:
        connection.close()
        print ('Closed Connection')
    
    except:
        print('ERROR! Could not Close')


##################################################
### Search dns_data files for match
##################################################
def searchDNS(host_name):
    for name in dns_data:
        if name == host_name:
            ip_value = '0x00 ' + str(dns_data[name+1])
            print ('Search Found: ',ip_value)

        else:
            ip_value = '0xFF'
    
    print ('ip_value: ',ip_value)
    return ip_value


##################################################
### Setting Up each Server and Handeling thier request 
# & replys to the client or other servers
##################################################
def requestSender(req): # req == [Client ID, hostname, I/R]

    while True:

        # Create Array version of req string / Check if user input is valid
        reqArray = req.split()
        print('reqArray length =', len(reqArray))

        # If program recives quit command leave this function
        if (str(reqArray[0]) == 'q'):
            reply = 'Connection Closed'
            break

        # 1st Error Check
        if (str(reqArray[2]) != 'r' and str(reqArray[2]) != 'i'):
            print('ERROR - Client did not specify an Iterative or Recursive request')
            # set reply as error message if invalid format has been entered by user
            reply = '0xEE' + ' ' + str(NAME) + ' ' + 'Invalid Format'
            break

        # Log request info from client && 2nd error check for user input
        try:
            createLogFile(str(reqArray[0]), ' ' + str(reqArray[1] + ' ' + str(reqArray[2])))
        except:
        # set reply as error message if invalid format has been entered by user
            reply = '0xEE' + ' ' + str(NAME) + ' ' + 'Invalid Format'
            break

    
    ######################################################################## 
    # Creating Default server
        if NAME == 'default':
            ### Socket Object for replaying information to other servers
            req_sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)


            req_sock.connect((server_dic['root'][0],server_dic['root'][1]))
            print('Connecting to Root Server')

            # relay request to other server and puase
            req_sock.send(str.encode(str(req)))
            open
            time.sleep(2)
            reply = req_sock.recv(2048)
            print('Reply == ', reply)
            break


    ########################################################################
    # Creating Root server: Make request from root to either com, org, or gov servers
        elif NAME == 'root':

            # create helper values for data searching
            search_value = str(reqArray[1][-3:]) # looks at last 3 characters of web address from client to determine the domain
            print ('search_value:', search_value)


            # Check for host name in this server and either returns value or lets user know value is missing with 0xFF
            #try:
            ip_value = searchDNS(reqArray[1])
            ip_value_array = ip_value.split()

            #Test ->
            print (ip_value_array)
            
            # Recursive Request
            if (reqArray[2] == 'r'):
                
                if (ip_value_array[0] == '0x00'):
                    reply = ip_value
                    break

                for name in server_dic:
                    if name == search_value:
                        # forloop searches for which server to connect to between com, org, or gov
                        req_sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
                        req_sock.connect((server_dic[name][0],server_dic[name][1]))
                        time.sleep(2)

                        req_sock.send(str.encode(str(req)))
                        time.sleep(2)
                        reply = req_sock.recv(2048)
                        time.sleep(1)
                        print (reply)
                        break
                break
            
            # Itterative Request
            elif reqArray[2] =='i':

                if (ip_value_array[0] == '0x00'):
                    reply = ip_value
                    break
                
                for name in server_dic:
                    if name == search_value:
                        reply = '0x01 ' + str(server_dic[name][0]) + ' ' + str(server_dic[name][1])
                        break
                break
    ######################################################################## 

    # Use for the com, org, gov servers 
        else:
            try:
                item = dns_data.index(reqArray[1])
                reply = '0x00' + ' ' + str(NAME) + ' ' +  str(dns_data[item+1])
            except:
                reply = '0xFF' + ' ' + str(NAME) + ' ' + 'Host Not Found'
            print (reply)
        break

    return reply
    

##################################################
### Function for handling multiple threads for requests
##################################################
def clientProcess (connection):

    #connection.send(str.encode('Your request has been recived on the ' + NAME + ' Server'))
    while True:
        # receive message array from client
        message = connection.recv(2048) #2048 = MAX buffer size
        request = messageProcess(str(message))
        print ("Client ID, HostName, I/R")
        print (str(request))

        # Send calculated reply and pause
        reply = requestSender(str (request))
        print ('Final reply: ', messageProcess(str(reply)))
        time.sleep(2)
        connection.send(str.encode(str(reply)))

        # Log server response
        createLogFile(NAME,reply)
        
        # close connection for all servers except for defualt server OR close if quit client sent Quit command 'q'
        if NAME != 'default' or request == 'q':
            closeConnection() 
            break

##################################################
### Accepting connections from a client
##################################################
while True:
    #connection = socket object from connecting client
    #addr = ip address info of connecting client
    connection,addr = s.accept()
    print('Connected to: '+addr[0]+':'+str(addr[1])) #prints ip and port client is using to connect to the server

    start_new_thread(clientProcess,(connection,))

