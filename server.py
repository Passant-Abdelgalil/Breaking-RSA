import socket
import RSA

host = socket.gethostname()
s = socket.socket() 
port=82
s.bind((host, port))  
# do not put ip so that it can here from any request
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(1)    
print ("server socket is listening, waiting for connectors")    

# Establish connection with userB.
userB, addr_acc = s.accept() 
print ('Got connection from', addr_acc )
 
# generate large prime number
arr=[76327548707654631819288365217926676480014891572829522940868712753524331330993,
    69456893419622706704072762858457751909086271322732082866554766081324404294541]
exponent = 23917

msg=''
# loop which accept all incoming connections 
while msg.lower().strip() != 'bye':

# recieve from client
    data = int(userB.recv(1024).decode())
    msg=RSA.RSA_Decrypt(data, arr[0], arr[1], exponent)
    print(msg)

# send to client
    text1=input() 
    ciphertext1 = RSA.RSA_Encrypt(text1, arr[0], arr[1], exponent)
    userB.send(str(ciphertext1).encode()) # send from server to client,appears at client

userB.close()