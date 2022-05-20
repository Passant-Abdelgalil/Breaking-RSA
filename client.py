import socket
import RSA

# generate large prime number
# generate public keys at client
arr=[76327548707654631819288365217926676480014891572829522940868712753524331330993,
    69456893419622706704072762858457751909086271322732082866554766081324404294541]
exponent = 23917
n=arr[0]* arr[1]
public_keys=[n, exponent]

host = socket.gethostname()
c = socket.socket() 
port=82

c.connect((host, port)) 

# send keys to server
c.send(str(public_keys[0]).encode()) 
c.send(' '.encode()) 
c.send(str(public_keys[1]).encode()) 


msg='' 

while msg.lower().strip() != 'bye':

# recieve from server
    data = int(c.recv(1024).decode())
    msg=RSA.RSA_Decrypt(data, arr[0], arr[1], exponent)
    print(msg)

c.close()