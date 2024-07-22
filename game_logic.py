from balloon import Balloon
from highscore import Highscore

"""
receiving bits overview

bit 0 (1.1): start_flag
bit 1 (1.2): end_flag
bit 2 (1.3): hit_flag balloon 1
bit 3 (1.4): miss_flag balloon 1
bit 4 (1.5): hit_flag balloon 2
bit 5 (1.6): miss_flag balloon 2
bit 6 (1.7): hit_flag balloon 3
bit 7 (1.8): miss_flag balloon 3
bit 8 (2.1): hit_flag balloon 4
bit 9 (2.2): miss_flag balloon 4
bit 10 (2.3): hit_flag balloon 5
bit 11 (2.4): miss_flag balloon 5
bit 12 (2.5): hit_flag balloon 6
bit 13 (2.6): miss_flag balloon 6
bit 14 (2.7): hit_flag balloon 7
bit 15 (2.8): miss_flag balloon 7
bit 16 (3.1): hit_flag balloon 8
bit 17 (3.2): miss_flag balloon 8
bit 18 (3.3): hit_flag balloon 9
bit 19 (3.4): miss_flag balloon 9
bit 20 (3.5): hit_flag balloon 10
bit 21 (3.6): miss_flag balloon 10
bit 22 (3.7): hit_flag balloon 11
bit 23 (3.8): miss_flag balloon 11
bit 24 (4.1): hit_flag balloon 12
bit 25 (4.2): miss_flag balloon 12
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
    start_flag_new = int(received[0])
    global end_flag
    end_flag_new = int(received[1])
    # read all other bits
    hit_miss_data = received[2:]
    print(received)
    # update game based on received bits
    if start_flag_new == 1 and start_flag_new != start_flag:
        # reset balloons and score-list
        for balloon in balloons:
            balloon.reset_balloon()
            
        for balloon in balloons:
            balloon.send_to_max(balloon.balloon_id, "background")

    elif end_flag_new == 1 and end_flag_new != end_flag:
        # update highscores
        
        scores = [(balloon.balloon_id, balloon.score) for balloon in balloons]
        daily_highscore.update_table(scores)
        season_highscore.update_table(scores)
        overall_highscore.update_table(scores)
        global daily_record
        daily_record = int(daily_highscore.top_five[0][0])
        global season_record
        season_record = season_highscore.top_five[0][0]
        global overall_record
        overall_record = overall_highscore.top_five[0][0]
        
        for balloon in balloons:
            balloon.send_to_max(balloon.balloon_id, "stop")

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
                #current_balloon.send_to_max("miss", channel_id=current_balloon.balloon_id)
            elif current_balloon.miss == 1 and miss == 0:
                # return to default
                current_balloon.miss = 0
            elif current_balloon.miss == 1 and miss == 1:
                # sent twice -> just ignore
                pass

    start_flag = start_flag_new
    end_flag = end_flag_new