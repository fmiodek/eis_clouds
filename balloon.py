# required sound format: mp3 with 44100 Hz
sound_hit = "sounds/hit.mp3"
sound_miss = "sounds/miss.mp3"
sound_streak = "sounds/streak.mp3"
sound_background = "sounds/background.mp3"

"""UDP"""
from pythonosc import udp_client

udp_ip = "127.0.0.1"
udp_port = 16575

# Create a client object
client = udp_client.SimpleUDPClient(udp_ip, udp_port)
print("udp client ready")


class Balloon:
    def __init__(self, balloon_id: int):
        self.balloon_id = balloon_id
        self.sequence = []
        self.score = 0
        self.streak = 0
        self.full_streak = False
        self.hit = 0
        self.miss = 0

    # reset ballon for new game
    def reset_balloon(self):
        self.sequence = []
        self.score = 0
        self.streak = 0
        self.full_streak = False
        self.hit = 0
        self.miss = 0

    def extend_sequence(self, hit_flag: int):
        self.sequence.append(hit_flag)

    def count_hits(self, hit_flag: int):
        self.score += hit_flag

    def check_streak(self, ongoing, streak_threshold: int):
        # increase streak if cloud was hit, otherwise set it to zero
        if ongoing == True:
            self.streak += 1
        else:
            self.streak = 0
        # check for special streak sound
        if self.streak > 0:
            if self.streak % streak_threshold == 0:
                self.full_streak = True

    def send_to_max(self, channel_id, sound_name):
        sound_id = -1
        if sound_name == "background":
            sound_id = 1
        elif sound_name == "hit":
            sound_id = 2
        elif sound_name == "collect":
            sound_id = 3
        elif sound_name == "loading":
            sound_id = 4
        elif sound_name == "stop":
            sound_id = 5
        
        elif sound_name == "mute":
            sound_id = 0
        elif sound_name == "unmute":
            sound_id = 100

        data_to_send = [channel_id, sound_id]
        print(data_to_send)
        client.send_message("/sound", data_to_send)

