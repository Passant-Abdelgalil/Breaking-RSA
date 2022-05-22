from RSA2 import RSA
import timeit
from helpers import ConvertToStr
import matplotlib.pyplot as plt
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("show_math_attack", help="flag to show/skip mathematical attack graph, Yes=> show, No=> skip", type=str)
    args = parser.parse_args()
    # Req3: encryption_time vs key_length graph
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
    plt.yticks(times)
    plt.title("RSA encryption time vs key length", fontsize=20)
    plt.show()

    # Req4: mathematical attack time vs key_length graph
    if args.show_math_attack.split("=")[-1].lower().strip() == "yes":            

        arr_nBits = [9, 12, 16, 18, 22]
        arr_message = ["a", "ab", "abc", 'abcd',
                    'ZZZZZ']
        arr_time = []
        arr_n = []
        for bit, message in zip(arr_nBits, arr_message):
            rsa = RSA(bits_number=bit)
            cipher = rsa.encrypt(message=message)
            arr_n.append(rsa.n)

            start = timeit.default_timer()
            msg_guessed_byAttacker = rsa.Math_Attack(
                cipher=cipher, n=rsa.n, e=rsa.e)
            time_taken = timeit.default_timer() - start

            arr_time.append(time_taken)
            print(
                f'time taken: {time_taken}, guessed message: {ConvertToStr(msg_guessed_byAttacker)} with bit length: {bit} and n: {rsa.n}')

        plt.title("Time(in seconds) taken by attack versus n")
        plt.plot(arr_n, arr_time, color="red")
        plt.ylabel("Time")
        plt.xlabel("n")
        plt.show()
