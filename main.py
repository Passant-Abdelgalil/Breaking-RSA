from RSA import ConvertToStr
from RSA2 import RSA
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="input file path", type=str)
    parser.add_argument(
        "--output_file", help="file path you wish to use to write outputs", type=str)
    args = parser.parse_args()

    input_file = args.input_file.split("=")[-1]
    print(input_file)
    if not os.path.isfile(input_file):
        print("file does not exist")
        exit(1)
    output_file = args.output_file if args.output_file else "./output.txt"

    print("""
          1 => run RSA
          2 => run Chosen Cipher Attack
          3 => run Mathematical Attack
          """)
    req_number = 0
    req_numbers = ["1", "2", "3"]
    try:
        while not (req_number in req_numbers):
            req_number = input('select requirement number to run:\n')
    except:
        print("exception")
        exit(1)

    output = open(output_file, 'w')
    rsa = RSA(file_path=input_file)

    if (req_number == "1"):
        cipher = rsa.encrypt(rsa.m)
        decrypted = ConvertToStr(rsa.decrypt(cipher))
        if decrypted != rsa.m:
            output.write(
                "ERROR: decrypted cipher doesn't match the plain text")

        output.write(f"PU = {{{rsa.e}, {rsa.n}}}\n")
        output.write(f"PR = {{{rsa.d}, {rsa.n}}}\n")
        output.write(f"E(PU, m) = {cipher}\n")
        output.write(f"D(PR, c) = {decrypted}\n")

    elif (req_number == "2"):
        cipher = rsa.encrypt(message=rsa.m)
        hacked_message, cipher_text = rsa.CCA(cipher=cipher)

        if(hacked_message != rsa.m):
            output.write(
                "ERROR: hacked message doesn't match the plain text\n")
        output.write(f"hacked message is:  {hacked_message}\n")
        output.write(f"message is: {rsa.m}\n")

    elif(req_number == "3"):
        cipher = rsa.encrypt(rsa.m)
        rsa.Math_Attack(cipher, rsa.n, rsa.e)
