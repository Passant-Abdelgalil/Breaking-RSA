import socket
# import import_ipynb
# import RSA

def PowMod(a, n, mod):
    if n == 0:
        return 1 % mod
    elif n == 1:
        return a % mod
    else:
        b = PowMod(a, n // 2, mod)
        b = b * b % mod
    if n % 2 == 0:
        return b
    else:
        return b * a % mod

def ConvertToInt(message_str):
    res = 0
    for i in range(len(message_str)):
        res = res * 256 + ord(message_str[i])
    return res



def ConvertToStr(n):
    res = ""
    while n > 0:
        res += chr(n % 256)
        n //= 256
    return res[::-1]

def extended_gcd(a,b):
    if b==0:
        d,x,y=a,1,0
    else:
        (d,p,q)=extended_gcd(b,a%b)
        x=q
        y=p-q* (a//b)
    return (d,x,y)

def RSA_Encrypt(m, p, q, e): #e:public exponent
    n=p*q
    c=PowMod( ConvertToInt(m) ,e ,n ) 
    return c

def RSA_Decrypt(c, p, q, e): #e:public exponent
    n=p*q
    phi_n=(p-1)*(q-1)
    result,x,y=extended_gcd(e,phi_n)
    d=x #d:private key
    if d < 0:
        d = (d % phi_n + phi_n) % phi_n # we don’t want −ve integers
    
    m=ConvertToStr( PowMod( c,d,n ) )
    return m



s = socket.socket() 
port=82
s.bind(('', port))  
# do not put ip so that it can here from any request
print ("socket binded to %s" %(port))
 
# put the socket into listening mode
s.listen(1)    
print ("socket is listening, waiting for userB")           
 
# loop which accept all incoming connections 
while True:

# Establish connection with userB.
    userB, addr = s.accept()    
    print ('Got connection from', addr )
    p = 1000000007
    q = 1000000009
    exponent = 23917
    ciphertext = RSA_Encrypt("TakeCareYouAreWatched", p, q, exponent)
    message = RSA_Decrypt(ciphertext, p, q, exponent)
    print(message)

    # send a thank you message to userB. encoding to send byte type.
    userB.send(message.encode())
    
    # Close the connection with userB
    userB.close()
    
    # Break the while loop once connection closed
    break