import socket
import time
import random
from pythonosc import dispatcher
from pythonosc import osc_server

from flask import Flask, jsonify, render_template
import threading
import time

from balloon import Balloon
from highscore import Highscore

HIT_POINTS = 10
AMOUNT_OF_BALLOONS = 12

# highscores
daily_highscore = Highscore("day")
season_highscore = Highscore("season")
overall_highscore = Highscore("overall")
daily_record = 0
season_record = 0
overall_record = 0

# init
start_flag = 2
end_flag = 2
sound_flag = 2
god_mode = 2

# instantiate the 12 balloons
balloons = [Balloon(id+1) for id in range(AMOUNT_OF_BALLOONS)]
currentScores = [99]*14
lock = threading.Lock()

"""TCP"""
IP = "192.168.76.150"
PORT = 50001

"""UDP"""
from pythonosc import udp_client

udp_ip = "127.0.0.1"
udp_port = 16575

# Create a client object
client_udp = udp_client.SimpleUDPClient(udp_ip, udp_port)
print("udp client 1 ready")

udp_port2 = 16577

"""
receiving bits overview

bit 0 (0.0): start_flag
bit 1 (0.1): end_flag
bit 2 (0.2): hit_flag balloon 1
bit 3 (0.3): collect_flag balloon 1
bit 4 (0.4): hit_flag balloon 2
bit 5 (0.5): collect_flag balloon 2
bit 6 (0.6): hit_flag balloon 3
bit 7 (0.7): collect_flag balloon 3
bit 8 (1.0): hit_flag balloon 4
bit 9 (1.1): collect_flag balloon 4
bit 10 (1.2): hit_flag balloon 5
bit 11 (1.3): collect_flag balloon 5
bit 12 (1.4): hit_flag balloon 6
bit 13 (1.5): collect_flag balloon 6
bit 14 (1.6): hit_flag balloon 7
bit 15 (1.7): collect_flag balloon 7
bit 16 (2.0): hit_flag balloon 8
bit 17 (2.1): collect_flag balloon 8
bit 18 (2.2): hit_flag balloon 9
bit 19 (2.3): collect_flag balloon 9
bit 20 (2.4): hit_flag balloon 10
bit 21 (2.5): collect_flag balloon 10
bit 22 (2.6): hit_flag balloon 11
bit 23 (2.7): collect_flag balloon 11
bit 24 (3.0): hit_flag balloon 12
bit 25 (3.1): collect_flag balloon 12
bit 26 (3.2): sound_flag -> 1:an 0:aus
bit 27 (3.3): god_mode -> 1:an 0:aus
"""

# take the received bits and update the game-state accordingly
def update_game(received: str):
    global start_flag
    global end_flag
    global sound_flag
    global god_mode

    global daily_record
    global season_record
    global balloons
    
    #print(received)
    # read bits
    start_flag_new = int(received[0])
    end_flag_new = int(received[1])
    hit_collect_data = received[2:]

    # check for god_mode
    
    god_mode_new = int(received[27])
    if god_mode_new == 1 and god_mode_new != god_mode:
        balloons[0].send_to_max(99, "god_mode", client_udp)
        god_mode = god_mode_new
    elif god_mode_new == 0 and god_mode_new != god_mode:
        god_mode = god_mode_new
    
        
    # read sound_flag bit and handle mute
    sound_flag_new = int(received[26])
    if sound_flag_new == 0 and sound_flag_new != sound_flag:
        balloons[0].send_to_max(0, "mute", client_udp)
        sound_flag = sound_flag_new
    elif sound_flag_new == 1 and sound_flag_new != sound_flag:
        balloons[0].send_to_max(0, "unmute", client_udp)
        sound_flag = sound_flag_new    
    
    # update game based on received bits
    if start_flag_new == 1 and start_flag_new != start_flag:
        # reset balloons and score-list
        for balloon in balloons:
            balloon.reset_balloon()
            
        for balloon in balloons:
            balloon.send_to_max(balloon.balloon_id, "stop", client_udp)
            balloon.send_to_max(balloon.balloon_id, "background", client_udp)

    elif end_flag_new == 1 and end_flag_new != end_flag:
        # update highscores
        """"
        scores = [(balloon.balloon_id, balloon.score) for balloon in balloons]
        daily_highscore.update_table(scores)
        season_highscore.update_table(scores)
        overall_highscore.update_table(scores)
        global daily_record
        daily_record = int(daily_highscore.best[0])
        global season_record
        season_record = int(season_highscore.best[0])
        global overall_record
        overall_record = int(overall_highscore.best[0])
        """
        for balloon in balloons:
            balloon.send_to_max(balloon.balloon_id, "stop", client_udp)
            balloon.send_to_max(balloon.balloon_id, "loading", client_udp)

    elif start_flag_new == 1 and end_flag_new == 0:
        # read hit/collect-bits for all balloons
        for i in range(0, AMOUNT_OF_BALLOONS*2, 2):
            current_balloon = balloons[i//2]
            hit = int(hit_collect_data[i])
            collect = int(hit_collect_data[i+1])
            # simulate edge trigger
            if current_balloon.hit == 0 and hit == 0:
                # nothing happens (except maybe a miss)
                pass
            elif current_balloon.hit == 0 and hit == 1:
                # cloud was hit
                current_balloon.hit = 1
                current_balloon.count_points(HIT_POINTS)
                current_balloon.send_to_max(current_balloon.balloon_id, "hit", client_udp)
            elif current_balloon.hit == 1 and hit == 0:
                # back to default
                current_balloon.hit = 0
            elif current_balloon.hit == 1 and hit == 1:
                # sent twice -> just ignore
                pass

            if current_balloon.collect == 0 and collect == 0:
                # nothing happended (except maybe a hit)
                pass
            elif current_balloon.collect == 0 and collect == 1:
                # clouds were colelcted / sucked in
                current_balloon.collect = 1
                # play collect sound
                current_balloon.send_to_max(current_balloon.balloon_id, "collect", client_udp)
            elif current_balloon.collect == 1 and collect == 0:
                # return to default
                current_balloon.collect = 0
            elif current_balloon.collect == 1 and collect == 1:
                # sent twice -> just ignore
                pass

    start_flag = start_flag_new
    end_flag = end_flag_new
    
    currScores = [3]*14
    currScores[0:12] = [balloon.score for balloon in balloons]
    currScores[12] = daily_record
    currScores[13] = season_record
    return currScores



def game_loop():
    global currentScores
    while True:
        
        i = 0
        while True:
            if i % 1000 == 0: 
                currentScores = [int(random.random()*100) for i in range(14)]
                i = 0
                #client_udp.send_message("/points", currentScores)
        """
        try:    
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((IP, PORT))
                # ready-message for the server
                ready = bytes([1]) #"Ready" in communication protocol
                sock.sendall(ready)
                    # receive data
                while True:
                    incoming_data = sock.recv(4)
                    if incoming_data:
                        # convert byte to bit-stream
                        received1 = ''.join(format(incoming_data[0], '08b'))
                        received2= ''.join(format(incoming_data[1], '08b'))
                        received3= ''.join(format(incoming_data[2], '08b'))
                        received4= ''.join(format(incoming_data[3], '08b'))
                        # reverse bytes and concat afterwards
                        received = received1[::-1] + received2[::-1] + received3[::-1] + received4[::-1]
                        
                        # handle received data, send response, or trigger actions
                        currentScores = update_game(received)
                        print("currentScores:", currentScores)
                        
                        # --> send data to frontend
                        
                    else: 
                        break

        except Exception as e:
            print("Error:", e)
            print("try reconnecting (from error)")
            sock.close()
            time.sleep(1)

        except KeyboardInterrupt:
            sock.close()
            break
            
        """

def message_handler(address, *args):
    print(f"Received message on {address} with arguments {args}")

def start_udp_server():
    # Erstelle einen Dispatcher und registriere den Handler für einen bestimmten OSC-Pfad
    disp = dispatcher.Dispatcher()
    disp.map("/", message_handler)

    # Erstelle den Server und gebe den Dispatcher und die Portnummer an
    server = osc_server.ThreadingOSCUDPServer(("localhost", udp_port2), disp)

    print("Server is listening...")
    server.serve_forever()


"""Frontend App"""
HOST = "192.168.76.152"
APP_PORT = 2207

app = Flask(__name__)

@app.route('/scores')
def scores():
    return render_template('scores.html')

@app.route('/score_data')
def score_data():
    global currentScores
    with lock:
        scores_copy = currentScores.copy()  # Kopie der Liste erstellen
    print("currentScores being sent:", scores_copy)  # Zum Debuggen
    return jsonify(scores_copy)
    #return jsonify(currentScores)


if __name__ == '__main__':
    
    game_thread = threading.Thread(target=game_loop)
    game_thread.daemon = True
    game_thread.start()

    server_thread = threading.Thread(target=start_udp_server)
    server_thread.start()

    app.run(host=HOST, port=APP_PORT, debug=True)
