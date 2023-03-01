from bluedot.btcomm import BluetoothServer
from signal import pause
from control_lab2 import Control2

def received_handler(data):

    cntl = Control2()
    try:
        if data != b"":
            print(data)  
            code = cntl.translate_bt(data)
            orientation, traveled = cntl.move(code)
            message= f"{orientation},{traveled}".encode('ascii')
            # s.send(message) # Echo back to client

    except: 
        print("Closing socket")
        s.close()

s = BluetoothServer(received_handler)

pause()