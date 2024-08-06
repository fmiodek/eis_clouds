import datetime

class Highscore:

    def __init__(self, time_span):
        self.time_span: str = time_span  # day / season / overall
        self.best = (0, 0, 0) # score, date, balloon_id
        self.got_new_score = False

    def read_table(self):
        file_path = "/Users/aufwind/eis_clouds/highscores/" + self.time_span + ".txt"
        #file_path = "eis_clouds/highscores/" + self.time_span + ".txt"
        with open(file_path, "r") as current_highscore:
            score_data = current_highscore.readline()    
            score, date, balloon_id = score_data.strip("\n").split(", ")
            self.best = (int(score), date, int(balloon_id))

    def check_new_scores(self, new_scores):
        current_date = datetime.datetime.now().date().strftime("%d.%m.%y")
        for new_score, balloon_id in new_scores:
            if new_score > self.best[0]:
                self.got_new_score = True
                self.best = (int(new_score), current_date, int(balloon_id))

    def write_table(self):
        file_path = "/Users/aufwind/eis_clouds/highscores/" + self.time_span + ".txt"
        #file_path = "eis_clouds/highscores/" + self.time_span + ".txt"
        with open(file_path, "w") as new_highscore:
            new_entry = str(self.best[0]) + ", " + self.best[1] + ", " + str(self.best[2]) + "\n"
            new_highscore.write(new_entry)

    def reset_table(self):
        current_date = datetime.datetime.now().date().strftime("%d.%m.%y")
        self.best = (0, current_date, 0)
        self.write_table()

    def update_table(self, new_scores):
        self.read_table()
        current_date = datetime.datetime.now().date().strftime("%d.%m.%y")
        # reset daily table if it´s a new day
        if self.time_span == "day":
            # reset if date is not equal to current date
            if self.best[1] != current_date:
                self.reset_table()
        # reset season table if its a new year
        elif self.time_span == "season":
            # reset if year of first entry is not equal to current year
            if self.best[1][-2:] != current_date[-2:]:
                self.reset_table()
        self.check_new_scores(new_scores)
        if self.got_new_score:
            self.write_table()
            self.got_new_score = False

