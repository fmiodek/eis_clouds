import socket
import time
import game_logic

IP = "192.168.178.48"
PORT = 3000

# while loop for automatic reconnecting if connection is lost
while True:
    # create tcp socket
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server
    try:
        client_sock.connect((IP, PORT))
        print(f"connected to server on {IP}:{PORT}")

        # ready-message for the server
        message = b"1"
        client_sock.sendall(message)

        # receive data
        while True:
            incoming_data = client_sock.recv(2)
            if incoming_data:
                # convert byte to bit-stream
                print("inc", incoming_data)
                received1 = ''.join(format(incoming_data[0], '08b'))
                received2= ''.join(format(incoming_data[1], '08b'))
                print("rec", received1 + received2)
                            
                # echo back?
                
                # handle received data, send response, or trigger actions
                #game_logic.update_game(received)
            else: 
                break

    except Exception as e:
        print("Error:", e)

    except KeyboardInterrupt:
        socket.close()
        break
        
    finally:
        socket.close()
        time.sleep(1)


