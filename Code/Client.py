import socket
import threading
import struct
from HelperFunction import *
import time
# Choosing Nickname
nickname = input("Choose your nickname: ")

# prepere the public and private key
print("RSA Encrypter/ Decrypter")
# p = int(input("Enter a prime number (17, 19, 23, etc): "))
# q = int(input("Enter another prime number (Not one you entered above): "))
n = int(input("number of bits: "))
print("Generating your public/private keypairs now . . .")
public, private = generate_key_pair_bits(n)
print("Your public key is ", public ," and your private key is ", private)
# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))
# Listening to Server and Sending Nickname
key_of_client = None
opponent_name = None
def receive():
    global key_of_client
    global opponent_name
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
                
            elif message == 'public_key':
                client.send(str(public).encode('utf-8'))
                
            elif message == 'key_size':
                client.send(str(n).encode('utf-8'))
                
            elif message.startswith('key') :
                key_of_client =eval(message[3:])
        
            elif message.startswith('name'):
                opponent_name = message[4:]
                
            elif message.startswith('chat'):
                messageChat = message[4:]
                messageChatArr = [int(num) for num in messageChat.split(',')]
                decrypted_message=[]
                start_time = time.time()
                for i in range(len(messageChatArr)):
                    decrypted_message.append(decrypt(messageChatArr[i], private))
                end_time = time.time()
                # print(f'the time of decryption is {end_time-start_time}')
                decoded_message=decode_message(decrypted_message)
                print(f'{opponent_name}: {decoded_message}')

        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break
# Sending Messages To Server
def write():
    while True:
        message= input('')
        print(f'{nickname}: {message}')
        crypted_Message =[]
        encoded_message = encode_message(message)
        # print("encoded_message : ",encoded_message)
        start_time = time.time()
        for i in range(len(encoded_message)):
            crypted_Message.append(encrypt(encoded_message[i], key_of_client))
        end_time = time.time()
        # print(f'the time of encryption is {end_time-start_time}')
        arr_string = ','.join(str(num) for num in crypted_Message)
        client.send(('chat'+arr_string).encode("utf-8"))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
