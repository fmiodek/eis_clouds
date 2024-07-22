import datetime

class Highscore:

    def __init__(self, time_span):
        self.time_span: str = time_span  # day / season / overall
        self.top_five: list[(int, str, int)] = [] # score, date, balloon_id
        self.header = "score, date, balloon_id\n"
        self.got_new_score = False

    def read_table(self):
        file_path = "highscores/" + self.time_span + ".txt"
        with open(file_path, "r") as current_highscore:
            current_highscore.readline()
            scores = current_highscore.readlines()
            for i in range(5):
                score, date, balloon_id = scores[i].strip("\n").split(", ")
                self.top_five.append((int(score), date, balloon_id))

    def check_new_scores(self, new_scores):
        current_date = datetime.datetime.now().date().strftime("%d.%m.%y")
        for balloon_id, new_score in new_scores:
            last_score = self.top_five[-1][0]
            if new_score > last_score:
                self.got_new_score = True
                self.top_five.pop()
                self.top_five.append((new_score, current_date, balloon_id))
                self.top_five = sorted(self.top_five, key=lambda triple: triple[0], reverse=True)

    def write_table(self):
        file_path = "highscores/" + self.time_span + ".txt"
        with open(file_path, "w") as new_highscore:
            new_highscore.writelines(self.header)
            print(self.top_five)
            for score, date, balloon_id in self.top_five:
                new_entry = str(score) + ", " + date + ", " + str(balloon_id) + "\n"
                new_highscore.write(new_entry)

    def reset_table(self):
        current_date = datetime.datetime.now().date().strftime("%d.%m.%y")
        self.top_five = []
        for i in range(5):
            reset_entry = (0, current_date, 0)
            self.top_five.append(reset_entry)
        self.write_table()

    def update_table(self, new_scores):
        self.read_table()
        current_date = datetime.datetime.now().date().strftime("%d.%m.%y")
        # reset daily table if it´s a new day
        if self.time_span == "day":
            # reset if date of first entry is not equal to current date
            if self.top_five[0][1] != current_date:
                self.reset_table()
        # reset season table if its a new year
        elif self.time_span == "season":
            # reset if year of first entry is not equal to current year
            if self.top_five[0][1][-2:] != current_date[-2:]:
                self.reset_table()
        self.check_new_scores(new_scores)
        if self.new_score:
            self.write_table()
            self.got_new_score = False

