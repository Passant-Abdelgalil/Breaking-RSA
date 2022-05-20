from RSA2 import *
from random import randint
rsa = RSA(bits_number=256)
message = "You are watched !"

cipher_text = rsa.encrypt(message=message)

RANDOM_NUMBER = randint(1, 50)

CHOSEN_CIPHER = rsa.encrypt(ConvertToStr(RANDOM_NUMBER))


hacked_message = rsa.decrypt(CHOSEN_CIPHER * cipher_text) // RANDOM_NUMBER



if(ConvertToStr(hacked_message) != message):
    print('Attack Failed!')
else:
    print('Attack Succeeded!')
    
# print(ConvertToStr(rsa.decrypt(cipher_text)))
print("hacked message is: ", ConvertToStr(hacked_message))
print("message is: ", message)

