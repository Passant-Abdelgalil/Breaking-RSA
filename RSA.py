
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

def RSA_Encrypt(m, n, e): #e:public exponent
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
	'''Generate a prime candidate divisibleby first primes'''
	while True:
		# Obtain a random number
		pc = nBitRandom(n)

		# Test divisibility by pre-generatedprimes
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

def generate_two_large_primes(n):
    arr=[0,0]
    for i in range(2):
        while True:
            # n = 256
            prime_candidate = getLowLevelPrime(n)
            if not isMillerRabinPassed(prime_candidate):
                continue
            else:
                # print(n, "bit prime is: \n", prime_candidate)
                arr[i]=prime_candidate
                break
    return arr

def generate_e(phi_n):
    d=0
    e=0
    while d != 1:
        e=random.randrange(2,phi_n)
        d,x,y=extended_gcd(e,phi_n)
        # print("e: ",e,"d: ",d, " x: ",x," y: ",y)
    return e
