import soundfile as sf
import numpy as np
import sounddevice as sd
import threading

sound_hit = "sounds/hit.mp3"
sound_miss = "sounds/miss.mp3"
sound_streak = "sounds/streak.mp3"
num_channels = 16
sample_rate = 44100

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

    # play the correct sound for each game situation
    def play_sound(self, sound_name: str, channel_id: int):
        def play_sound_thread(sound_name, channel_id):
            sound_file = ""
            if sound_name == "streak":
                sound_file = sound_streak
            elif sound_name == "hit":
                sound_file = sound_hit
            elif sound_name == "miss":
                sound_file = sound_miss

            audio_data, sr = sf.read(sound_file)
            print("Original audiofile sample rate:", sr)
            print("Original audiofile shape:", audio_data.shape)

            # If the number of channels is different, repeat to match num_channels
            if audio_data.shape[1] != num_channels:
                audio_data = np.repeat(audio_data, num_channels/2, axis=1)

            # Convert the audio data to the same data type
            # audio_data_mp3 = audio_data_mp3.astype(np.float32)  

            print("Final audiofile shape:", audio_data.shape)

            # Select only the audio data for the selected channel (0-indexed)
            audio_data_to_play = audio_data[:, channel_id]

            # Play the audio on the selected channel (1-indexed)
            sd.play(audio_data_to_play, samplerate=sample_rate, mapping=[channel_id+1])

            # Wait until playback is finished
            status = sd.wait()
            print("Playback status:", status)
        
        thread = threading.Thread(target=play_sound_thread, args=(sound_name, channel_id))
        thread.start()
        

#test_balloon0 = Balloon(0)
#test_ballono1 = Balloon(1)
#test_balloon0.play_sound("streak", channel_id=11)
#test_ballono1.play_sound("streak", channel_id=9)

