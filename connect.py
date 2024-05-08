import socket
import time
import game_logic

IP = "192.168.1.100"
PORT = 50001

# while loop for automatic reconnecting if connection is lost
while True:
    # create tcp socket
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    try:
        print("try connecting")
        client_sock.connect((IP, PORT))
        print(f"connected to server on {IP}:{PORT}")

        # ready-message for the server
        ready = bytes([1])  # 10000000 -> reversed 
        client_sock.sendall(ready)
        print("sent:", bin(int.from_bytes(ready, byteorder='big'))[2:].zfill(8))

        # receive data
        while True:
            incoming_data = client_sock.recv(2)
            if incoming_data:
                # convert byte to bit-stream
                received1 = ''.join(format(incoming_data[0], '08b'))
                received2= ''.join(format(incoming_data[1], '08b'))
                received = received1 + received2
                received = received[::-1]
                print("received:", received)
                
                # handle received data, send response, or trigger actions
                game_logic.update_game(received)
            else: 
                break

    except Exception as e:
        print("Error:", e)
        "try reconnecting (from error)"
        client_sock.close()
        time.sleep(1)

    except KeyboardInterrupt:
        client_sock.close()
        break
        
    finally:
        "try reconnecting (from finally)"
        client_sock.close()
        time.sleep(1)
        


