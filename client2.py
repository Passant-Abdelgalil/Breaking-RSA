import socket
import argparse
from helpers import ConvertToStr

from RSA2 import RSA

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("bits", help="key length", type=int)
    args = parser.parse_args()
    # generate public keys at client
    rsa = RSA(bits_number=int(args.bits))

    arr = [rsa.p, rsa.q]
    exponent = rsa.e
    n = rsa.n
    public_keys = [n, exponent]

    host = socket.gethostname()
    c = socket.socket()
    port = 82

    c.connect((host, port))

    # send keys to server
    keys = f"{str(public_keys[0])} {str(public_keys[1])}"
    c.send(keys.encode())

    msg = ''

    while msg.lower().strip() != 'bye':

        # receive from server
        data = int(c.recv(1024).decode())
        msg = rsa.decrypt(data, arr[0], arr[1], exponent)
        msg = ConvertToStr(msg)
        print(f"Received message after decryption is: {msg}")

    c.close()
