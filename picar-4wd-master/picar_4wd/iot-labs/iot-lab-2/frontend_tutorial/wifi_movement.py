import socket
from control_lab2 import Control2

HOST = "192.168.50.217" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    cntl = Control2()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)  
                orientation, traveled, obstacle = cntl.move(data)
                message= f"{orientation},{traveled},{obstacle}".encode('ascii')
                client.sendall(message) # Echo back to client
    except Exception as e:
        print('error: ', e)
        print("Closing socket")
        client.close()
        s.close()