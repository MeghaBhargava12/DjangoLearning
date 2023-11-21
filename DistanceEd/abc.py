import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Random.random import getrandbits
from Crypto.Hash import SHA256

##### DH parameters
p = 2582249878086908589655919172003011874329705792829223512830659356540647622016841194629645353280137831435903171972747559779
g = 2


### generate deffie helman key (part 4.b)
def gen_df_key():
    private_key = getrandbits(400)
    public_key = pow(g, private_key, p)
    return private_key, public_key


###### get the shared key using private key and public key of peer
def get_shared_key(private_key, other_public_key):
    return pow(other_public_key, private_key, p)


def main():
    server_ip = '127.0.0.1'
    server_port = 12349

    ## part 4.a

    ##create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)

    print("Server is listening on {}:{}".format(server_ip, server_port))

    conn, addr = server_socket.accept()
    print("Connected to client:", addr)

    #### part 4.b

    # generate deffie-hellman keys
    private_key, public_key = gen_df_key()

    # send the public key to the other user
    conn.send(str(public_key).encode())

    # get the other user public key
    client_public_key = int(conn.recv(4096).decode())

    # get the shared key
    shared_key = get_shared_key(private_key, client_public_key)

    ## create the seckret key using SHA256
    secret_key = SHA256.new(str(shared_key).encode()).digest()

    print("Secret Key(server): " + secret_key)


    while True:
        print("waitng for data from other side....")

        data = conn.recv(4096)
        ciphertext_length = int.from_bytes(data[:4], 'big')
        tag_length = int.from_bytes(data[4:8], 'big')
        ciphertext = data[8:8 + ciphertext_length]
        received_tag = data[8 + ciphertext_length:8 + ciphertext_length + tag_length]
        nonce = data[8 + ciphertext_length + tag_length:]

        ## create aes cipher for decrypt with same nonce used for encryption
        aes_cipher = AES.new(secret_key, AES.MODE_EAX, nonce=nonce)
        decrypted_message = aes_cipher.decrypt(ciphertext)

        ### part 4.d

        # create new tag and verify with received tag
        new_tag = SHA256.new(ciphertext).digest()

        ## if tags dont match
        if new_tag != received_tag:
            print("Tags doesn't match, message might be tampered")
        else:
            print("Client message:", decrypted_message.decode())  # Convert to string for display

        ## get aes cipher object
        aes_cipher = AES.new(secret_key, AES.MODE_EAX)

        ### send some message
        message = input("You: ")

        #### part 4.c

        # Encrypt the message and compute the tag
        ciphertext = aes_cipher.encrypt(message.encode('utf-8'))
        print("C (ciphertext): " + ciphertext)
        ## create the tag
        tag = SHA256.new(ciphertext).digest()

        ## message to send length of text + length of tag+ text+ tag+ nonce for aes
        message_to_send = len(ciphertext).to_bytes(4, 'big') + len(tag).to_bytes(4,
                                                                                 'big') + ciphertext + tag + aes_cipher.nonce

        ## send this message
        conn.send(message_to_send)

if __name__ == "__main__":
    main()
