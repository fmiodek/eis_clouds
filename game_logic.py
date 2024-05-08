import balloon

"""
receiving bits overview

bit 0: start_flag
bit 1: end_flag
bit 2: hit_flag
bit 3: miss_flag
bit 4: balloon 1
bit 5: balloon 2
bit 6: balloon 3
bit 7: balloon 4
bit 8: balloon 5
bit 9: balloon 6
bit 10: balloon 7
bit 11: balloon 8
bit 12: balloon 9
bit 13: balloon 10
bit 14: balloon 11
bit 15: balloon 12
"""

# amount of consecutive hits until a special sound is played
STREAK_THRESHOLD = 3

# instantiate the 12 balloons
balloons = [balloon.Balloon(id) for id in range(12)]

# take the received bits and update the game-state accordingly
def update_game(received: str):
    # filter out non-logical receives:
    if received[4:16] == "0"*12 and received[0:2] == "00":
        return

    # read first 4 bits
    start_flag = int(received[0])
    end_flag = int(received[1])
    hit_flag = int(received[2])
    miss_flag = int(received[3])    

    # update game based on received bits
    if start_flag:
        for balloon in balloons:
            balloon.reset_balloon()
    elif end_flag:
        pass
    else:
        current_balloon_id = int(received[4:16].index("1")) 
        current_balloon = balloons[current_balloon_id]
        current_balloon.extend_sequence(hit_flag)
        current_balloon.count_streak(hit_flag, STREAK_THRESHOLD)
        if current_balloon.is_streak:
            current_balloon.play_sound("streak", channel_id=current_balloon_id, volume=1.0)
            current_balloon.is_streak = False
        else:
            if hit_flag:
                current_balloon.play_sound("hit", channel_id=current_balloon_id, volume=1.0)
            else:
                current_balloon.play_sound("miss", channel_id=current_balloon_id, volume=1.0)

        