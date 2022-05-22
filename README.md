# Implementing-Cracking_RSA
Use python to implement RSA encryption algorithm then use different methods to crack it.

## Two Ways of cracking
### 1. Mathematical Attack
Attack is done by trying to know the the two prime factors of n, 
so we can get Phi_n, and then get d (private key) to decrypt the message.

### 2. Chosen Ciphertext Attack (CCA) 

## Run
To run RSA, CCA, MA, use:
```
python main.py input_file="input.txt" --output_file="output.txt"
```
if it gives error then use python3 instead of python

To run the communication, open two terminals, then write in order:
```
python sender.py  
```
```
python receiver.py 256
```
write in the sender terminal and see the message in the receiver terminal.

