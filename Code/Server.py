import socket
import threading
from HelperFunction import *
import time

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
PublicKeys = []
number_of_bits_of_key=[]
time_of_attack=[]
time_of_encryption=[]
time_of_decryption=[]

# define the attack function
def attack(public_key,name,key_size):
    start_time = time.time()
    e,n=public_key
    factors = []
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    # return factors
    p = factors[0]-1
    q=factors[1]-1
    phi = (p)*(q)
    d=multiplicative_inverse(e,phi)
    end_time = time.time()
    print(f'from attacker .. for {name} the private key is {d} the time is {end_time-start_time} for the key of size {key_size} bits')
# Sending Messages To All Connected Clients
def broadcast(message,client):
    for member in clients:
        # print(member,client)
        if member != client:
            member.send(message)
# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            
            message = client.recv(1024)
            
            broadcast(message,client)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clintName = clients[index]
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            publicKey = PublicKeys[index]
            # broadcast('{} left!'.format(nickname).encode('utf-8'),client)
            nicknames.remove(nickname)
            PublicKeys.remove(publicKey)
            break
# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
  
        # Request And Store Nickname
        
        # public_key
        client.send('public_key'.encode('utf-8'))
        
        public_key = client.recv(1024).decode('utf-8')
        # my_tuple = pickle.loads(data)
        PublicKeys.append(public_key)
        
        # key_size
        client.send('key_size'.encode('utf-8'))
        
        key_size = client.recv(1024).decode('utf-8')
        number_of_bits_of_key.append(key_size)
        
        # public key
        attack_thread = threading.Thread(target=attack(eval(public_key),nickname,key_size))
        attack_thread.start()
        clients.append(client)
        if(len(clients)==2):
            clients[0].send(('key'+PublicKeys[1]).encode('utf-8'))
            clients[1].send(('key'+PublicKeys[0]).encode('utf-8'))
            clients[0].send(('name'+nicknames[1]).encode('utf-8'))
            clients[1].send(('name'+nicknames[0]).encode('utf-8'))
            # print('key Server'+PublicKeys[1])
        # print(f'Nickname is {nickname} and public key is {public_key}')
        # broadcast("{} joined!".format(nickname).encode('utf-8'),client)
        # client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
receive()