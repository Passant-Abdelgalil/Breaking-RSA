from RSA2 import RSA
import timeit
from helpers import ConvertToStr
import matplotlib.pyplot as plt


if __name__ == "__main__":
    bits = [32, 64, 128, 256]
    times = []
    for bits_number in bits:
        message = str(bits_number) + "bits"
        rsa = RSA(bits_number=bits_number)
        starting_time = timeit.default_timer()
        cipher = rsa.encrypt(message=message)
        ending_time = timeit.default_timer()
        times.append((ending_time - starting_time) * 1000)
        print("message is ", message)
        print("decrypted message is ", ConvertToStr(rsa.decrypt(cipher)))

    plt.figure(figsize=(12, 8))
    plt.plot(bits, times)
    plt.xlabel("key length", fontsize=18)
    plt.ylabel("Encryption time in milliseconds", fontsize=18)
    plt.xticks(bits)
    plt.title("RSA encryption time vs key length", fontsize=20)
    plt.show()
    