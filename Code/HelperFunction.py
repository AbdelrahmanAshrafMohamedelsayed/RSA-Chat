from cmath import sqrt
from math import floor
from random import randint
import time
import random
import matplotlib.pyplot as plt

# map characters to numbers
mapping = {
     'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19,
    'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29,
    'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35, ' ': 36,
    'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16, 'h': 17, 'i': 18, 'j': 19,
    'k': 20, 'l': 21, 'm': 22, 'n': 23, 'o': 24, 'p': 25, 'q': 26, 'r': 27, 's': 28, 't': 29,
    'u': 30, 'v': 31, 'w': 32, 'x': 33, 'y': 34, 'z': 35,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'0':0
}
inverseMapping = {v: k for k, v in mapping.items()}

def char_to_num(char):
    return mapping.get(char, 36)

def num_to_char(num):
    if 0 <= num <= 36:
        return list(mapping.keys())[list(mapping.values()).index(num)]
    else:
        return ' '

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
def extended_euclidean_algorithm(a, b):

    if a == 0:
        return (b, 0, 1)
    if b == 0:
        return (a, 1, 0)

    r0 = a
    r1 = b
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1

    while r1 != 0:
        q = r0 // r1  
        r0, r1 = r1, r0 - q * r1
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    return (r0, x0, y0)
def multiplicative_inverse(a, m):

    gcd, x, y = extended_euclidean_algorithm(a, m)
    if gcd != 1:
        raise ValueError(f"{a} there is no multiplicative inverse modulo {m}")
    else:
        return x % m
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def encode_message(message):
    
    # append spaces to fill out the last grouping
    while len(message) % 5 != 0:
        message += ' '
    # convert extra characters to spaces
    message = message.replace('\n', ' ')
    message = message.replace('\t', ' ')
    message = message.replace('\r', ' ')
    # replace any characters that are not letter or space or number with a space
    
    
    # group the plaintext into sets of five characters per group
    groups = [message[i:i+5] for i in range(0, len(message), 5)]
    
    # convert each group into a separate number
    numbers = []
    for group in groups:
        number = 0
        for i in range(4, -1, -1):
            if i < len(group):
                number += char_to_num(group[i]) * (37 ** (4 - i))
        numbers.append(number)
    # return plaintext_number
    return numbers

# generate the keys
# key size 
def Get_Prime(bit_length):
    number = randint(2**(bit_length-1), 2**bit_length-1)
    while not is_prime(number):
        number = randint(2**(bit_length-1), 2**bit_length-1)
    return number
def generate_key_pair_bits(bit_length):
    # Generate two prime numbers of bit_length bits
    p = Get_Prime(bit_length)
    q = Get_Prime(bit_length)
    while p == q:
        q = Get_Prime(bit_length)
    return generate_keypair(p,q)

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal")

    n = p * q
    phi = (p-1) * (q-1)

    e = random.randrange(1, phi)
    # e=7

    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = multiplicative_inverse(e, phi)
# (e, n) is the public key and (d, n) is the private key.
    return ((e, n), (d, n))

def encrypt(M, pk):
    if pk is None:
        raise ValueError("Public key cannot be None")
    e, n = pk
    cipher =pow(M, e, n)
    return cipher

def decrypt(C, pr):
    d, n = pr
    Plaintext = pow(C, d, n)

    return Plaintext

def decode_message(ciphertext_numbers):
    # convert each number back to its original character grouping
    groups = []
    for number in ciphertext_numbers:
        group = ""
        for i in range(4, -1, -1):
            if number >= 37**i:
                # convert the largest multiple of 37^i to a character and subtract it from the number
                group += num_to_char(number // (37**i))
                number %= 37**i
            else:
                # if the number is too small, add a space character
                group += " "
        groups.append(group)
    # concatenate the character groupings to form the original message
    return "".join(groups)

# def attack(public_key,name):
    
#     e,n=public_key
#     factors = []
#     i = 2
#     while i * i <= n:
#         if n % i:
#             i += 1
#         else:
#             n //= i
#             factors.append(i)
#     if n > 1:
#         factors.append(n)
#     # return factors
#     p = factors[0]-1
#     q=factors[1]-1
#     phi = (p)*(q)
#     d=multiplicative_inverse(e,phi)
#     print(f'for {name} the private key is {d}')
# attack((65537,11*13),'alice')
# break_times = [0.10503053665161133,0.21868205070495605,0.33296895027160645,0.9122836589813232,1.7068846225738525,2.9657740592956543,7.6004180908203125,14.993981838226318,27.61822247505188,54.1855103969574,97.76128602027893]
# key_sizes = [20,21,22,23,24,25,26,27,28,29,30]

# plt.plot(key_sizes, break_times)
# plt.xlabel('Key Size (bits)')
# plt.ylabel('Algorithm Breaking Time (seconds)')
# plt.title('Algorithm Breaking Time vs Key Size')
# plt.show()
# def big_encrypt(message,key):
#     # public, private = generate_key_pair_bits(keySize)
#     crypted_Message =[]
#     encoded_message = encode_message(message)
#     # print(encoded_message)
#     for i in range(len(encoded_message)):
#         crypted_Message.append(encrypt(encoded_message[i], key))
        
#     return crypted_Message
# def big_decrypt(crypted_Message,key):
#     # public, private = generate_key_pair_bits(keySize)
#     decoded_message = []
#     for i in range(len(crypted_Message)):
#         decoded_message.append(decrypt(crypted_Message[i], key))
#     return decode_message(decoded_message)
# # for drawing the graph of decryption time vs key size


# # for drawing the graph of encryption time vs key size
# x = []
# y = []
# z=[]
# for i in range(20, 50, 1):
#     public, private = generate_key_pair_bits(i)
#     start = time.time()
#     ciphertext = big_encrypt("attacknowmanfatherfumuerloserqwertyuiopasdfghjklzxcvbnm",public)
#     print(ciphertext)
#     end = time.time()
#     start2=time.time()
#     print(big_decrypt(ciphertext,private))
#     end2=time.time()
#     # decrypt
#     x.append(i)
#     y.append(end-start)
#     z.append(end2-start2)
#     print(i)

# plt.plot(x, y)
# plt.xlabel('Key Size (bits)')
# plt.ylabel('encryption Time (seconds)')
# plt.title('encryption Time Time vs Key Size')
# plt.show()
# plt.plot(x, z)
# plt.xlabel('Key Size (bits)')
# plt.ylabel('decryption Time (seconds)')
# plt.title('decryption Time Time vs Key Size')
# plt.show()