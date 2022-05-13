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
    res = ''
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

# Large Prime Generation for RSA
import random

# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
					31, 37, 41, 43, 47, 53, 59, 61, 67,
					71, 73, 79, 83, 89, 97, 101, 103,
					107, 109, 113, 127, 131, 137, 139,
					149, 151, 157, 163, 167, 173, 179,
					181, 191, 193, 197, 199, 211, 223,
					227, 229, 233, 239, 241, 251, 257,
					263, 269, 271, 277, 281, 283, 293,
					307, 311, 313, 317, 331, 337, 347, 349]

def nBitRandom(n):
	return random.randrange(2**(n-1)+1, 2**n - 1)

def getLowLevelPrime(n):
	'''Generate a prime candidate divisible
	by first primes'''
	while True:
		# Obtain a random number
		pc = nBitRandom(n)

		# Test divisibility by pre-generated
		# primes
		for divisor in first_primes_list:
			if pc % divisor == 0 and divisor**2 <= pc:
				break
		else: return pc

def isMillerRabinPassed(mrc):
	'''Run 20 iterations of Rabin Miller Primality test'''
	maxDivisionsByTwo = 0
	ec = mrc-1
	while ec % 2 == 0:
		ec >>= 1
		maxDivisionsByTwo += 1
	assert(2**maxDivisionsByTwo * ec == mrc-1)

	def trialComposite(round_tester):
		if pow(round_tester, ec, mrc) == 1:
			return False
		for i in range(maxDivisionsByTwo):
			if pow(round_tester, 2**i * ec, mrc) == mrc-1:
				return False
		return True

	# Set number of trials here
	numberOfRabinTrials = 20
	for i in range(numberOfRabinTrials):
		round_tester = random.randrange(2, mrc)
		if trialComposite(round_tester):
			return False
	return True




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
arr=[0,0]
for i in range(2):
    while True:
        n = 256
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            # print(n, "bit prime is: \n", prime_candidate)
            arr[i]=prime_candidate
            break
exponent = 23917


# loop which accept all incoming connections 
while True:

    text1=input() + '\n'
    # ciphertext1 = RSA_Encrypt(text1, arr[0], arr[1], exponent)
    

    # At userB. encoding to send byte type.
    # message1 = RSA_Decrypt(ciphertext1, arr[0], arr[1], exponent)
    # message1 = message1 +' '
    userB.send(text1.encode()) # send from server to client,appears at client

    data = userB.recv(1024)
    while userB.recv(1024) != b'\r\n':
        data= data+ userB.recv(1024)
        print(data.decode())
    
    print(data.decode())# send from client to server,appears at server
    #userB.send(data)# send from server to client,appears at client

    # userB.send(message1.encode())
    
    # Close the connection with userB
    # userB.close()
    
    # Break the while loop once connection closed
    # break