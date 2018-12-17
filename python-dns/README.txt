##############################################
# Kris Bliss
# ID: 5215031
# bliss132@umn.edu
###############################################

### Concept of Program
    The prorgam works as follows:
        - The 'dns.py' file is used to emulate every DNS sever for this project.
        - The 'client.py' file will use a modified 'user_input.txt' provided in the submission.
        - The DNS servers take a simplifed version of the DNS queries from the project requirnments and preform either an Itterative search.
           or a Recursive search for the ip corresponding to a host name provided by the client program.
        - All modifcation made are due to features of the project that have been hardcoded or could not be prefected before the due date.
          Explinations for them will be provied in the "How to Run this Project" section of this 'README.txt'.


### How to Run this Project
    1) open minimum of 4 terminals and go to directory of my assignment in each
    2) run commands "py dns.py <name of server>" in first 3 terminals and "py client.py <Client ID number> <IP to connect to> <Port to connect to>" in last terminal.
    
	2.a) Starting the Servers
		Command: py dns.py <Names/IDs of server>
        Names/IDs of servers are: (Must use exact names)
        - default (replacement name for defualt_local)
        - root
        - com
        - gov
        - org
		
    2.b) 
		#Info and Explinations about the servers
        - The servers are hardcoded to know which Host ip and ports they will need to use.
        - Note: Though that info is hardcoded, it has not eliminated the need of the 'server.dat' for in the 
		  root server as that information is used in fucntion searchDNS() to find out which server to send its request to.
		- This project assumes that the root and default servers do not have any stored information about host/ip data so they
		  both try to either get information from the .com, .org, or .gov servers or tell user where to find the information.
		- The program will resond to user with all message types specified in requirements (i.e. 0x00, 0x01, 0xEE, 0xFF) but is not perfect
		  interms of error catching.
		- All connections close after a response is sent.
		- Lots of sleep fucntions are used to ensure that data is sent and recived accross ports properly. 
		  This causes the program to take about 10-15 secs to complete each request.
		- The servers do not take file inputs but know what files to read/create. 
		  Make sure all server and user_input files are in the same directory as project.
		- All orignial server files should work fine for this portion of the project
		
		
		#Nuances	
		- Each server will log data as specified in the project but these logs must be deleted by hand when servers are terminated to refresh their state.
		- For itterative requests, the root server sends back the host and port information the client should connect to for getting the correct ip information
		  but the default server will not make that request for the user. The user will have to submit a new request with newly provided information.

			
    3) Follow prompt on Client to make a request in format <web address> <i/r> (ex: www.google.com R).
	4) To end the client program and disconnect from default server, type 'q' and submit to have program shut down and close its ports.
	
	4.a) Nuances of Client
		- The client will have its ID preprogramed to be added to its dns requests as it will take that ID data from the initialization process in step 2.
		- For every request, the user will have to quit the client and restart program to submit a new request. 
		- I have provied an alternative 'user_input' file in the final submission.
		  I will place my header into it to verify it is mine, but you may have to remove the header for the program to work.
		
   

