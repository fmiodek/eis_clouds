import socket
import time
import game_logic

IP = "192.168.76.150"
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
        ready = bytes([128]) # 10000000 -> "Ready" in communication protocol
        client_sock.sendall(ready)
        print("sent:", bin(int.from_bytes(ready, byteorder='little'))[2:].zfill(8))

        # receive data
        while True:
            incoming_data = client_sock.recv(4)
            if incoming_data:
                # convert byte to bit-stream
                received1 = ''.join(format(incoming_data[0], '08b'))
                received2= ''.join(format(incoming_data[1], '08b'))
                received3= ''.join(format(incoming_data[2], '08b'))
                received4= ''.join(format(incoming_data[3], '08b'))
                # reverse bytes and concat afterwards
                received = received1[::-1] + received2[::-1] + received3[::-1] + received4[::-1]
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
        


