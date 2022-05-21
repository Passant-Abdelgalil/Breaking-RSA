import random
from helpers import *
import re
from random import randint


class RSA:

    def __init__(self, bits_number_or_file_path):
        if isinstance(bits_number_or_file_path, int):
            self.generate_primes(bits_number=bits_number_or_file_path)
            # compute rsa public key
            self.n = self.p * self.q
            # compute rsa Euler's totient function
            self.phi = (self.p - 1) * (self.q - 1)
            # generate private keys e and d
            self.e, self.d = self.generate_e_d(self.phi)

        elif isinstance(bits_number_or_file_path, str):
            self.p = None
            self.q = None
            self.e = None
            self.n = None
            self.phi = None
            self.m = None
            self.c = None
            with open(bits_number_or_file_path, 'r') as f:
                parameter_regex = "^\s*[q, p, e, c]\s*=\s*[0-9]+"
                text_regex = "^\s*[m]\s*=\s*.+"
                for line in f:
                    user_input = re.search(parameter_regex, line)
                    if user_input is None:
                        user_input = re.search(text_regex, line)
                    if user_input is None:
                        continue
                    try:
                        user_input = user_input.group()
                        user_input = user_input.strip()
                        if user_input[0] == "p":
                            self.p = int(re.split("=\s*", user_input)[-1])
                        elif user_input[0] == "q":
                            self.q = int(re.split("=\s*", user_input)[-1])
                        elif user_input[0] == "e":
                            self.e = int(re.split("=\s*", user_input)[-1])
                        elif user_input[0] == "m":
                            self.m = re.split("=\s*", user_input)[-1]
                        elif user_input[0] == "c":
                            self.c = int(re.split("=\s*", user_input)[-1])
                    except:
                        continue
                if (self.p == None) or (self.q == None) or (self.e == None) or (self.m == None) or (self.c == None):
                    print("input file is invalid")
                    exit(1)
                self.n = self.p * self.q
                self.phi = (self.p - 1) * (self.q - 1)
                _, self.d = self.generate_e_d(self.phi, e=self.e)

    def encrypt(self, message, p=None, q=None, e=None):
        self.m = message
        message = ConvertToInt(message)
        n = None
        if (p is not None) and (q is not None) and (e is not None):
            n = p * q
        else:
            n = self.n
            e = self.e

        if(message >= n):
            print("message %d is >= modulus %d" % (message, n))
        return PowMod(message, e, n)

    def decrypt(self, cipher, p=None, q=None, e=None):
        d = None
        n = None
        phi_n = None
        if (p is not None) and (q is not None) and (e is not None):
            print("decrypt has input")
            phi_n = (p - 1) * (q - 1)
            d = self.calc_d(phi_n=phi_n, e=e)
            n = p * q
        else:
            d = self.d
            n = self.n
            phi_n = self.phi
        if d < 0:
            # we don’t want −ve integers
            d = (d % phi_n + phi_n) % phi_n

        return PowMod(cipher, d, n)

    def generate_e_d(self, phi_n, e=None):
        if e is not None:
            _, inverse_modulo, _ = extended_gcd(e, phi_n)
        else:
            gcd = 0
            e = 0
            inverse_modulo = None
            # loop till gcd(e, phi) = 1
            while gcd != 1:
                # generate random number in range >= 1 && < phi
                e = random.randrange(1, phi_n - 1)
                # compute gcd(e, phi)
                gcd, inverse_modulo, y = extended_gcd(e, phi_n)
        return e, inverse_modulo

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

    def CCA(self, message=None):
        prev_message = self.m
        if message is not None:
            cipher_text = self.encrypt(message=message)
        else:
            cipher_text = self.encrypt(message=prev_message)

        RANDOM_NUMBER = randint(1, 10)

        CHOSEN_CIPHER = self.encrypt(message=ConvertToStr(RANDOM_NUMBER))

        self.m = prev_message
        
        hacked_message = self.decrypt(
            cipher=CHOSEN_CIPHER * cipher_text) // RANDOM_NUMBER
        return ConvertToStr(hacked_message), cipher_text

    def Math_Attack(self, cipher, n, e):
        for p in range(1, n):
            if n % p == 0:
                if(self.Miller_Rabin_Primality_Test(p)):
                    q = n//p
                    m = self.decrypt(cipher, p, q, e)
                    c1 = self.encrypt(m, p, q, e)
                    if c1 == cipher:
                        return m
        return "can't know the message"
