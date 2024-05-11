import datetime

class Highscore:
    def __init__(self, time_span):
        self.time_span: str = time_span  # day / season / overall
        self.top_five: list[(int, str, int)] = []
        self.header = "score, date, balloon_id\n"

    def read_table(self):
        file_path = "highscores/" + self.time_span + ".txt"
        with open(file_path, "r") as current_highscore:
            current_highscore.readline()
            scores = current_highscore.readlines()
            for score_data in scores:
                score, date, balloon_id = score_data.strip("\n").split(", ")
                self.top_five.append((int(score), date, balloon_id))

    def check_new_scores(self, new_scores: list[int]):
        current_date = datetime.datetime.now().date().strftime("%d.%m.%y")
        for balloon_id, new_score in enumerate(new_scores):
            last_score = self.top_five[-1][0]
            if new_score > last_score:
                self.top_five.pop()
                self.top_five.append((new_score, current_date, balloon_id))
                self.top_five = sorted(self.top_five, key=lambda triple: triple[0], reverse=True)

    def write_table(self):
        file_path = "highscores/" + self.time_span + ".txt"
        with open(file_path, "w") as new_highscore:
            new_highscore.writelines(self.header)
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
        #reset daily table if it´s a new day
        if self.time_span == "day":
            current_date = datetime.datetime.now().date().strftime("%d.%m.%y")
            if self.top_five[0][1] != current_date:
                self.reset_table()
        self.check_new_scores(new_scores)
        self.write_table()


#test_score = Highscore("day")
#new_scores = [0,0,0,0,0,55,0,0,23,0,0,10]
#test_score.update_table(new_scores)



