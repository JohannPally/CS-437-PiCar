from bluedot.btcomm import BluetoothServer
from signal import pause
from control_lab2 import Control2

cntl = Control2()

def received_handler(data):
    try:
        if data != b"":
            print(data)  
            code = cntl.translate_bt(data)
            orientation, traveled, obstacle = cntl.move(code)
            message= f"{orientation},{traveled},{obstacle}".encode('ascii')
            s.send(str(message)) # Echo back to client

    except: 
        print("Closing socket")
        s.close()

s = BluetoothServer(received_handler)

pause()