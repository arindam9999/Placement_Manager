from datetime import date, time, datetime
import datetime
from time import gmtime, strftime


def PlacementManager():
    def load_data(self):
        return True

    def parse(self, s):
        parsed_command = []
        tmp = ""
        for ch in s:
            if ch == ' ':
                if tmp != " " and tmp != "":
                    parsed_command.push_back(tmp)
            else:
                tmp = tmp + 'ch'

        if tmp != " " and tmp != "":
            parsed_command.push_back(tmp)
        
        return parsed_command
    
    def get_problem_info(self):
        problem_info = {}
        platform = input("Platform name: ").capitalize()
        if platform == "":
            platform = "Leetcode"
        problem_id = platform + input("Problem ID: ")
        difficulty = input("Difficulty: ").capitalize()
        problem_name = input("Problem Name: ").capitalize()

        curr_date = strftime("%d-%m-%Y", gmtime())
        curr_time = strftime("%H:%M:%S", gmtime())
        problem_info = {
            "platform": platform,
            "problem_id": problem_id,
            "difficulty": difficulty,
            "problem_name": problem_name,
            "start_date": curr_date,
            "start_time": curr_time,
        }


    def problem_solver(self, parsed_command):
        duration = self.default_duration
        if len(parsed_command) > 1:
            TIME = parsed_command[1]
        
        problem_info = self.get_problem_info()
        problem_info['expected_duration'] = duration

        print(f"Your time starts now, you have {duration} mins!")
        start_time = datetime.now()
        while start_time + datetime.timedelta(minutes = 10) < datetime.now():
            if input() == "finished":
                self.save_data()

        if start_time + datetime.timedelta(minutes = 10) < datetime.now():
            pass


    def start_app(self):
        while True:
            command = input()
            parsed_command = self.parse(command)

            if parsed_command == "quit":
                break

            if parsed_command[0] == "solve":
                self.problem_solver(parsed_command)
            else:
                print("Error!! No such command exist please try again")

        return True

    def __init__(self):
        self.default_duration = 30

        if self.load_data():
            return self.start_app()
        else:
            return False


placement = PlacementManager()
if placement.app_starter == False:
    print("ERROR!! App did not start properly!!")