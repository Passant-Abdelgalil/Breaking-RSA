import socket
import RSA

# generate large prime number
arr=[76327548707654631819288365217926676480014891572829522940868712753524331330993,
    69456893419622706704072762858457751909086271322732082866554766081324404294541]
exponent = 23917

host = socket.gethostname()
c = socket.socket() 
port=82

c.connect((host, port)) 

text2=''
while text2.lower().strip() != 'bye':

# send to server
    text2=input() 
    ciphertext2 = RSA.RSA_Encrypt(text2, arr[0], arr[1], exponent)
    c.send(str(ciphertext2).encode()) 

# recieve from server
    data = int(c.recv(1024).decode())
    msg=RSA.RSA_Decrypt(data, arr[0], arr[1], exponent)
    print(msg)

c.close()