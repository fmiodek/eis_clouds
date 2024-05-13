from balloon import Balloon
from highscore import Highscore

"""
receiving bits overview

bit 0: start_flag
bit 1: end_flag
bit 2: hit_flag balloon 1
bit 3: miss_flag balloon 1
bit 4: hit_flag balloon 2
bit 5: miss_flag balloon 2
bit 6: hit_flag balloon 3
bit 7: miss_flag balloon 3
bit 8: hit_flag balloon 4
bit 9: miss_flag balloon 4
bit 10: hit_flag balloon 5
bit 11: miss_flag balloon 5
bit 12: hit_flag balloon 6
bit 13: miss_flag balloon 6
bit 14: hit_flag balloon 7
bit 15: miss_flag balloon 7
bit 16: hit_flag balloon 8
bit 17: miss_flag balloon 8
bit 18: hit_flag balloon 9
bit 19: miss_flag balloon 9
bit 20: hit_flag balloon 10
bit 21: miss_flag balloon 10
bit 22: hit_flag balloon 11
bit 23: miss_flag balloon 11
bit 24: hit_flag balloon 12
bit 25: miss_flag balloon 12
"""

# amount of consecutive hits until a special sound is played
STREAK_THRESHOLD = 3
AMOUNT_OF_BALLOONS = 12

# highscores
daily_highscore = Highscore("day")
season_highscore = Highscore("season")
overall_highscore = Highscore("overall")

# instantiate the 12 balloons
balloons = [Balloon(id) for id in range(AMOUNT_OF_BALLOONS)]

# take the received bits and update the game-state accordingly
def update_game(received: str):
    # read first 2 bits
    start_flag = int(received[0])
    end_flag = int(received[1])
    hit_miss_data = received[2:AMOUNT_OF_BALLOONS*2]
   
    # update game based on received bits
    if start_flag:
        # reset balloons and score-list
        for balloon in balloons:
            balloon.reset_balloon()
    elif end_flag:
        # update highscores
        scores = [balloon.score for balloon in balloons]
        daily_highscore.update_table(scores)
        season_highscore.update_table(scores)
        overall_highscore.update_table(scores)
    else:
        # read hit/miss-bits for all balloons
        for i in range(0, AMOUNT_OF_BALLOONS*2, 2):
            current_balloon = balloons[i]
            hit = int(hit_miss_data[i])
            miss = int(hit_miss_data[i+1])

            # simulate edge trigger
            if current_balloon.hit == 0 and hit == 0:
                # nothing happens (except maybe a miss)
                pass
            elif current_balloon.hit == 0 and hit == 1:
                # cloud was hit
                current_balloon.hit = 1
                current_balloon.extend_sequence(1)
                current_balloon.count_hits(hit)
            elif current_balloon.hit == 1 and hit == 0:
                # back to default
                current_balloon.hit = 0
            elif current_balloon.hit == 1 and hit == 1:
                # sent twice -> just ignore
                pass

            if current_balloon.miss == 0 and miss == 0:
                # nothing happended (except maybe a hit)
                pass
            elif current_balloon.miss == 0 and miss == 1:
                # cloud was missed
                current_balloon.miss = 1
                current_balloon.extend_sequence(0)
            elif current_balloon.miss == 1 and miss == 0:
                # return to default
                current_balloon.miss = 0
            elif current_balloon.miss == 1 and miss == 1:
                # sent twice -> just ignore
                pass

        
        
        """
        TODO: check for streak direkt bei edge trigger
        current_balloon.count_streak(STREAK_THRESHOLD)

        TODO: überarbeiten!! funktioniert so nicht mehr
        Sound muss direkt bei edge trigger abgespielt werden
        
        # play sounds depending on game situation
        if current_balloon.is_streak:
            current_balloon.play_sound("streak", channel_id=current_balloon.id, volume=1.0)
            current_balloon.is_streak = False
        else:
            if hit_flag == 1:
                current_balloon.play_sound("hit", channel_id=current_balloon_id, volume=1.0)
            elif miss_flag == 1:
                current_balloon.play_sound("miss", channel_id=current_balloon_id, volume=1.0)
        """