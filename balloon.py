class Balloon:
    def __init__(self, balloon_id: int):
        self.balloon_id = balloon_id
        self.score = 0
        self.hit = 0
        self.collect = 0

    # reset ballon for new game
    def reset_balloon(self):
        self.score = 0
        self.hit = 0
        self.collect = 0

    def count_points(self, hit_points: int):
        self.score += hit_points
        print(self.balloon_id, self.score)

    def send_to_max(self, channel_id, sound_name, udp_client):
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
        elif sound_name == "god_mode":
            sound_id = 6
        
        elif sound_name == "mute":
            sound_id = 0
        elif sound_name == "unmute":
            sound_id = 100

        data_to_send = [channel_id, sound_id]
        print(data_to_send)
        udp_client.send_message("/sound", data_to_send)

