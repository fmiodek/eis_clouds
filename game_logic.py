from balloon import Balloon
from highscore import Highscore

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

# amount of consecutive hits until a special sound is played
HIT_POINTS = 1
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

# take the received bits and update the game-state accordingly
def update_game(received: str):
    global start_flag
    global end_flag
    global sound_flag
    global god_mode

    print(received)

    # read bits
    start_flag_new = int(received[0])
    end_flag_new = int(received[1])
    hit_collect_data = received[2:]

    # check for god_mode
    
    god_mode_new = int(received[27])
    if god_mode_new == 1 and god_mode_new != god_mode:
        balloons[0].send_to_max(99, "god_mode")
        god_mode = god_mode_new
    elif god_mode_new == 0 and god_mode_new != god_mode:
        god_mode = god_mode_new
    
        
    # read sound_flag bit and handle mute
    sound_flag_new = int(received[26])
    if sound_flag_new == 0 and sound_flag_new != sound_flag:
        balloons[0].send_to_max(0, "mute")
        sound_flag = sound_flag_new
    elif sound_flag_new == 1 and sound_flag_new != sound_flag:
        balloons[0].send_to_max(0, "unmute")
        sound_flag = sound_flag_new    
    
    # update game based on received bits
    if start_flag_new == 1 and start_flag_new != start_flag:
        # reset balloons and score-list
        for balloon in balloons:
            balloon.reset_balloon()
            
        for balloon in balloons:
            balloon.send_to_max(balloon.balloon_id, "stop")
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
        for balloon in balloons:
            balloon.send_to_max(balloon.balloon_id, "stop")
            balloon.send_to_max(balloon.balloon_id, "loading")

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
                current_balloon.send_to_max(current_balloon.balloon_id, "hit")
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
                current_balloon.send_to_max(current_balloon.balloon_id, "collect")
            elif current_balloon.collect == 1 and collect == 0:
                # return to default
                current_balloon.collect = 0
            elif current_balloon.collect == 1 and collect == 1:
                # sent twice -> just ignore
                pass

    start_flag = start_flag_new
    end_flag = end_flag_new