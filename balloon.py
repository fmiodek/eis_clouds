import soundfile as sf
import numpy as np
import sounddevice as sd

sound_hit = "sounds/hit.mp3"
sound_miss = "sounds/miss.mp3"
sound_streak = "sounds/streak.mp3"
num_channels = 8
sample_rate = 44100

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
    def play_sound(self, sound_name: str, channel_id: int):
        sound_file = ""
        if sound_name == "streak":
            sound_file = sound_streak
        elif sound_name == "hit":
            sound_file = sound_hit
        elif sound_name == "miss":
            sound_file = sound_miss

        audio_data_mp3, sr_mp3 = sf.read(sound_file)
        print("Original MP3 sample rate:", sr_mp3)
        print("Original MP3 shape:", audio_data_mp3.shape)

        # Convert the audio data to the same sample rate and number of channels as the dummy data
        if sr_mp3 != sample_rate:
            audio_data_mp3 = sf.resample(audio_data_mp3, sample_rate, axis=0)

        # If the number of channels is different, repeat to match num_channels
        if audio_data_mp3.shape[1] != num_channels:
            audio_data_mp3 = np.repeat(audio_data_mp3, num_channels/2, axis=1)

        # Convert the audio data to the same data type
        # audio_data_mp3 = audio_data_mp3.astype(np.float32)  

        print("Final MP3 shape:", audio_data_mp3.shape)

        # Select only the audio data for the selected channel (0-indexed)
        audio_data_to_play = audio_data_mp3[:, channel_id]

        # Play the audio on the selected channel [1-indexed]
        sd.play(audio_data_to_play, samplerate=sample_rate, mapping=[channel_id+1])

        # Wait until playback is finished
        status = sd.wait()
        print("Playback status:", status)
        

test_balloon = Balloon(0)
test_balloon.play_sound("streak", channel_id=4)

