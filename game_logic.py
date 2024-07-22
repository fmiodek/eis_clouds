from balloon import Balloon
from highscore import Highscore

"""
receiving bits overview

bit 0 (0.0): start_flag
bit 1 (0.1): end_flag
bit 2 (0.2): hit_flag balloon 1
bit 3 (0.3): miss_flag balloon 1
bit 4 (0.4): hit_flag balloon 2
bit 5 (0.5): miss_flag balloon 2
bit 6 (0.6): hit_flag balloon 3
bit 7 (0.7): miss_flag balloon 3
bit 8 (1.0): hit_flag balloon 4
bit 9 (1.1): miss_flag balloon 4
bit 10 (1.2): hit_flag balloon 5
bit 11 (1.3): miss_flag balloon 5
bit 12 (1.4): hit_flag balloon 6
bit 13 (1.5): miss_flag balloon 6
bit 14 (1.6): hit_flag balloon 7
bit 15 (1.7): miss_flag balloon 7
bit 16 (2.0): hit_flag balloon 8
bit 17 (2.1): miss_flag balloon 8
bit 18 (2.2): hit_flag balloon 9
bit 19 (2.3): miss_flag balloon 9
bit 20 (2.4): hit_flag balloon 10
bit 21 (2.5): miss_flag balloon 10
bit 22 (2.6): hit_flag balloon 11
bit 23 (2.7): miss_flag balloon 11
bit 24 (3.0): hit_flag balloon 12
bit 25 (3.1): miss_flag balloon 12
bit 26 (3.2): sound_flag -> 1:an 0:aus
"""

# amount of consecutive hits until a special sound is played
HIT_POINTS = 1
STREAK_POINTS = 3
STREAK_THRESHOLD = 3
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

# instantiate the 12 balloons
balloons = [Balloon(id+1) for id in range(AMOUNT_OF_BALLOONS)]

# take the received bits and update the game-state accordingly
def update_game(received: str):
    # read first 2 bits
    global start_flag
    global end_flag
    start_flag_new = int(received[0])
    end_flag_new = int(received[1])
   
    # read sound_flag bit
    sound_flag = int(received[26])
    if sound_flag == 0:
        for balloon in balloons:
                balloon.send_to_max(balloon.balloon_id, "stop")
    
    # read all other bits for balloon data
    hit_miss_data = received[2:]
    print(received)
    # update game based on received bits
    if start_flag_new == 1 and start_flag_new != start_flag:
        # reset balloons and score-list
        for balloon in balloons:
            balloon.reset_balloon()
            
        if sound_flag == 1:
            for balloon in balloons:
                balloon.send_to_max(balloon.balloon_id, "background")

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
        if sound_flag == 1:
            for balloon in balloons:
                balloon.send_to_max(balloon.balloon_id, "loading")

    elif start_flag_new == 1 and end_flag_new == 0:
        # read hit/miss-bits for all balloons
        for i in range(0, AMOUNT_OF_BALLOONS*2, 2):
            current_balloon = balloons[i//2]
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
                current_balloon.check_streak(True, STREAK_THRESHOLD)
                if current_balloon.full_streak:
                    # play streak sound
                    current_balloon.send_to_max(current_balloon.balloon_id, "hit")
                    current_balloon.full_streak = False
                    current_balloon.score += STREAK_POINTS
                else:
                    # play hit sound
                    current_balloon.send_to_max(current_balloon.balloon_id, "hit")
                    current_balloon.score += HIT_POINTS    
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
                current_balloon.check_streak(False, STREAK_THRESHOLD)
                # play miss sound
                current_balloon.send_to_max(current_balloon.balloon_id, "collect")
            elif current_balloon.miss == 1 and miss == 0:
                # return to default
                current_balloon.miss = 0
            elif current_balloon.miss == 1 and miss == 1:
                # sent twice -> just ignore
                pass

    start_flag = start_flag_new
    end_flag = end_flag_new