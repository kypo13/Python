import socket
import select

HEADER_LENGTH = 10
#chat dengan server local
IP = "127.0.0.1"
PORT = 1234

#AF = Address Family
#Buat socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

#manage list client

sockets_list = [server_socket]

#client dictionary / client socket -> key
clients = {}

def receive_message(client_socket):
    try:
        #menampung panjang message
        message_header = client_socket.recv(HEADER_LENGTH)

        #kalau gak terima message close
        if not len(message_header):
            return False

        #typecasting ke interger
        message_length = int(message_header.decode("utf-8").strip())

        #return message
        return {"header": message_header, "data": client_socket.recv(message_length)}


    except:
        return False

#recieve message
#select.select(apa yang pingin dibaca dan dapat data darimana, apa yang dibaca, mau dimasukan kemana)
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    for notified_socket in read_sockets:
        #kalau connect
        if notified_socket == server_socket:
            #membuat koneksi baru
            client_socket, client_address = server_socket.accept()

            #recieve username dari client
            user = receive_message(client_socket)
            #kalau disconnect
            if user is False:
                continue

            #nambah list socket        
            sockets_list.append(client_socket)

            #menyimpan username
            clients[client_socket] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
        
        else:
            #menerima pesan
            message = receive_message(notified_socket)

            #kalau client disconnect
            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                #remove socket
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            
            user = clients[notified_socket]
            
            print(f"Receive Message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
        
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    
    #remove exception socket
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]