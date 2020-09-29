import socket
import select
import errno
import sys

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234

my_username = input("Masukan Username: ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connect ke ip yang di set
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

#mengirim informasi ke server dan encode ke bytes
username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

while True:
    #input user dari client
    message = input(f"{my_username} : ")
    #message = ""
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        #mengirim pesan
        client_socket.send(message_header + message)

    try:
        while True:
            #menerima pesan
            username_header = client_socket.recv(HEADER_LENGTH)
            #kalau dapat pesan dari tempat lain
            if not len(username_header):
                print('Koneksi terputus dari server')
                sys.exit()
            #menerima username
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")

            #check message
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")

            #print pesan
            print(f"{username} : {message}")

    #kalau ada error
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error',str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error',str(e))
        sys.exit()