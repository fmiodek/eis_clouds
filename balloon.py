import pygame

sound_hit = "sounds/hit.mp3"
sound_miss = "sounds/miss.mp3"
sound_streak = "sounds/streak.mp3"

class Balloon:
    def __init__(self, balloon_id: int):
        self.balloon_id = balloon_id
        self.sequence = []
        self.score = 0
        self.streak = 0
        self.is_streak = False

    # reset ballon for new game
    def reset_balloon(self):
        self.sequence = []
        self.score = 0
        self.streak = 0
        self.is_streak = False

    def extend_sequence(self, hit_flag: int):
        self.sequence.append(hit_flag)

    def count_hits(self, hit_flag: int):
        self.score += hit_flag

    def count_streak(self, hit_flag, miss_flag: int, streak_threshold: int):
        # increase streak if cloud was hit, otherwise set it to zero
        if hit_flag == 1 and miss_flag == 0:
            self.streak += 1
        elif hit_flag == 0 and miss_flag == 1:
            self.streak = 0
        # check for special streak sound
        if self.streak > 0:
            if self.streak % streak_threshold == 0:
                self.is_streak = True

    # play the correct sound for each game situation
    def play_sound(self, sound_name: str, channel_id: int, volume: float):
        file = ""
        if sound_name == "streak":
            file = sound_streak
        elif sound_name == "hit":
            file = sound_hit
        elif sound_name == "miss":
            file = sound_miss
        
        pygame.mixer.init()
        sound = pygame.mixer.Sound(file)
        sound.set_volume(volume)
        channel = pygame.mixer.Channel(channel_id)
        channel.play(sound)

        return sound.get_length()
    

#test_balloon = Balloon(0)
#duration = test_balloon.play_sound("streak", channel_id=0, volume=1.0)
# Keep the program running to allow the sound to play
#pygame.time.wait(int(duration * 1000))  # Wait for the duration of the sound