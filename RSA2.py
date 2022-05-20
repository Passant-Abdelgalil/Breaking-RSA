from ast import Pow
import random
from helpers import *


class RSA:

    def __init__(self, bits_number):
        self.generate_primes(bits_number=bits_number)
        # compute rsa public key
        self.n = self.p * self.q
        # compute rsa Euler's totient function
        self.phi = (self.p - 1) * (self.q - 1)
        # generate private keys e and d
        self.generate_e_d(self.phi)

    def encrypt(self, message):
        message = ConvertToInt(message)
        if(message >= self.n):
            print("message %d is >= modulus %d" % (message, self.n))
        return PowMod(message, self.e, self.n)

    def decrypt(self, cipher):

        if self.d < 0:
            # we don’t want −ve integers
            self.d = (self.d % self.phi + self.phi) % self.phi

        return PowMod(cipher, self.d, self.n)

    def generate_e_d(self, phi_n):
        gcd = 0
        e = 0
        inverse_modulo = None
        # loop till gcd(e, phi) = 1
        while gcd != 1:
            # generate random number in range >= 1 && < phi
            e = random.randrange(1, phi_n - 1)
            # compute gcd(e, phi)
            gcd, inverse_modulo, y = extended_gcd(e, phi_n)
        # store randomly generate e as the rsa exponent (first private key)
        self.e = e
        # store the inverse modulo of e as the rsa second private key
        self.d = inverse_modulo

    def generate_primes(self, bits_number):
        x = random.getrandbits(bits_number)
        while not self.Miller_Rabin_Primality_Test(x, iterations=20):
            x = x + 1
        self.p = x

        x = random.getrandbits(bits_number)
        while not self.Miller_Rabin_Primality_Test(x, iterations=20):
            x = x + 1
        self.q = x

    def Miller_Rabin_Primality_Test(self, candidate_prime, iterations=20):
        """
        Mailler Rabin Algorithm is:
        ============================
        1- Find n-1 = 2**k * m, where n is the number to test its primality
        2. for 'iterations'
            2-1 choose a such that 1 < a < n-1
            2-2 Testing loop: for 'k' iterations
                - compute b0 = a**m (mod n)
                - if b = 1: then n is not a prime
                - if b = -1 then n is a prime
                - else iterate for s iterations with b_i = (b_i-1)**2 (mod n)
        """
        if candidate_prime == 2:
            return True
        # if the number is even, return false
        if not(candidate_prime & 1):
            return False

        # factorize  candidate_prime - 1 into 2**k *m where m is a prime number
        p1 = candidate_prime - 1
        k = 0
        m = p1
        # while m is even
        while m % 2 == 0:
            # shift to right by 1 which is equivalent to division by 2
            m >>= 1
            # increase the exponent
            k += 1
        # n-1 = 2**k * m should hold
        assert candidate_prime - 1 == 2**k * m

        def witness(a, loop_size):
            """
            iterate for (s iterations) = loop_size, starting with b0 = a**m (mod n)
                - if b_i = 1: then n is not a prime
                - if b_i = -1 then n is a prime
                - if b_i = n - 1 break 
                - else update b_i = (b_[i-1])**2 (mod n)
            """
            b_i = PowMod(a, m, candidate_prime)
            for _ in range(loop_size):
                if b_i == 1:
                    return False
                elif b_i == -1:
                    return True
                elif b_i == candidate_prime - 1:
                    return False
                b_i = PowMod(b_i, 2, candidate_prime)

            return True

        for _ in range(iterations):
            # pick random integer in range [2, candidate_prime - 2]
            a = random.randrange(2, candidate_prime - 2)
            # perform witness loop checking
            if(witness(a, k)):
                return False

        return True
