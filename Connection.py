import socket
import RSA


s = socket.socket() 
port=82
s.bind(('', port))  
# do not put ip so that it can here from any request
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(1)    
print ("socket is listening, waiting for connectors")    

# Establish connection with userB.
userB, addr_acc = s.accept() 
print ('Got connection from', addr_acc )
 
# generate large prime number
arr=RSA.generate_two_large_primes()
exponent = 23917


# loop which accept all incoming connections 
while True:

    text1=input() + '\r\n'
    ciphertext1 = RSA.RSA_Encrypt(text1, arr[0], arr[1], exponent)
    

    # At userB. encoding to send byte type.
    # message1 = RSA_Decrypt(ciphertext1, arr[0], arr[1], exponent)
    # message1 = message1 +' '
    userB.send(RSA.RSA_Decrypt(ciphertext1, arr[0], arr[1], exponent).encode()) # send from server to client,appears at client

    # data = userB.recv(1024)
    # while userB.recv(1024) != b'\r\n':
    #     data= data+ userB.recv(1024)
    #     print(data.decode())
    
    # print(data.decode())# send from client to server,appears at server
    #userB.send(data)# send from server to client,appears at client

    # userB.send(message1.encode())
    
    # Close the connection with userB
    # userB.close()
    
    # Break the while loop once connection closed
    # break