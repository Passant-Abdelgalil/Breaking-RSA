from RSA import *
from random import randint
import math
rsa = RSA(p=1000000007, q=1000000009, e=23917)

message = "Take"

cipher_text = rsa.encrypt(message=message)

RANDOM_NUMBER = randint(1, int(math.log(cipher_text)))

CHOSEN_CIPHER = rsa.encrypt(ConvertToStr(RANDOM_NUMBER))


hacked_message =  rsa.decrypt(CHOSEN_CIPHER * cipher_text) // RANDOM_NUMBER


# print(ConvertToStr(rsa.decrypt(cipher_text)))
print("hacked message is: ", ConvertToStr(hacked_message))
print("message is: ", message)

if(hacked_message != message):
    print('Attack Failed!')
else:
    print('Attack Succeeded!')
    
    