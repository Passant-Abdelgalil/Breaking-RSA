# Implementing-Cracking_RSA
<img src="https://img.shields.io/badge/Language-python-blue" alt="Website" />
Use python to implement RSA encryption algorithm then use different methods to crack it.

## RSA Encryption(message,n, exponent):
1. Setup message(M) for encryption (Convert message to integer)
2. Public key{n,e}, e: exponent
3. Get cipher C = 𝑀^𝑒 𝑚𝑜𝑑 𝑛 using powMod function

## RSA Decryption(c,p,q,e):
1. Private key{p,q}
2. Compute n, n=p*q
3. Compute Φ(n)=(p-1)*(q-1)
4. We know that e.d=1 mod Φ(n) so get d as the inverse of e mod Φ(n)
5. M=𝐶^𝑑 𝑚𝑜𝑑 𝑛

## Communication
* We used **socket** programming.
* At the sender, we initialize a host and port and then begin listening waiting for the receiver.
* At the receiver, it makes the private key{p.q}, generate exponent, connect with the sender with its host and port, and first send the public key{n,e}, where n=p*q so that the sender could send the messages encrypted using the public key. The receiver waits for the sender to send messages so it can decrypt them.
* Whenever the sender gets a connection, it receives the public key and then uses it to encrypt messages and send them to the receiver.

## Two Ways of cracking
### 1. Mathematical Attack
The attack goal is to retrieve the original plain-text message by getting the key value. It depends
on factorizing the public key ‘n’. The Algorithm is as follows:
1. To know the first prime(p), try numbers from 2 until n
2. Take p whenever two conditions are satisfied:
    a. n is divisible by p
    b. p is a prime number
3. Get the second prime(q) where q=n//p
4. Decrypt the cypher the attacker has with the attacker generated private keys(p&q), to get
a message
5. Encrypt this message, to get cypher text
6. Compare the attacker generated cypher with the original cypher, if they meet then those
were the correct private keys, and the message in step 4 is correct.
7. If it’s not correct, repeat from step 2 until it finds the correct message or it reaches n and
couldn’t know the message.

### 2. Chosen Ciphertext Attack (CCA) 
The attack goal is to retrieve the original plain-text message regardless of the key value.
The Algorithm is as follows:
1. Intercept the communication between two entities.
2. Choose random integer number ‘r’
3. Encrypt ‘r’ with the RSA public key as 𝑟^𝑒 𝑚𝑜𝑑 𝑛
4. Multiply the encrypted r with the received ciphertext modulo n to get (𝑀^𝑒) * (𝑟^𝑒) 𝑚𝑜𝑑 𝑛
5. Send the result to the right entity.
6. The entity responds with (𝑀^𝑒 * 𝑟^𝑒)𝑑 𝑚𝑜𝑑 𝑛
7. Knowing that e*d=1 mod Φ(n), this gives that the received message is actually M*r modn
8. Divide it by the randomly generated number ‘r’ to obtain the original message.
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

