from helpers import *

class RSA:
    
    def __init__ (self, p, q, e):
        self.p = p
        self.q = q
        self.e = e
        self.n = p * q
        self.phi = (p-1) * (q-1)
        
    def encrypt(self, message):
        message = ConvertToInt(message)
        if(message >= self.n):
            print("message %d is >= modulus %d"%(message, self.n))
        return PowMod(message, self.e, self.n)
    
    def decrypt(self, cipher):
        
        _, private_key, _ = extended_gcd(self.e, self.phi)
        
        if private_key < 0:
            private_key = (private_key % self.phi + self.phi) % self.phi # we don’t want −ve integers
                
        return PowMod( cipher,private_key,self.n )
        
