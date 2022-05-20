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

# recieve the keys from client
public_keys=0 # n,e
public_keys=userB.recv(1024).decode()
n=int(public_keys.split(' ')[0])
e=int(public_keys.split(' ')[1])

text1=''
# loop which accept all incoming connections 
while text1.lower().strip() != 'bye':

# send to client
    text1=input() 
    ciphertext1 = RSA.RSA_Encrypt(text1, n, e)
    userB.send(str(ciphertext1).encode()) 

userB.close()