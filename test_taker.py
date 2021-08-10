from datetime import date, time, datetime, timedelta
import json
from time import gmtime, strftime
import keyboard
from playsound import playsound

class PlacementManager:
    def parse(self, s):
        parsed_command = []
        tmp = ""
        for ch in s:
            if ch == ' ':
                if tmp != " " and tmp != "":
                    parsed_command.append(tmp)
                    tmp = ""
            else:
                tmp = tmp + ch

        if tmp != " " and tmp != "":
            parsed_command.append(tmp)
        
        return parsed_command

    def load_data(self):
        with open('data.json', 'r') as handle:
            self.data = json.load(handle)
        handle.close()

        dump_flag = False
        curr_date = strftime("%d-%m-%Y", gmtime())
        if 'total_problems_solved' not in self.data:
            self.data['total_problems_solved'] = 0
            dump_flag = True

        if 'total_contests_attended' not in self.data:
            self.data['total_contests_attended'] = 0
            dump_flag = True

        if 'total_upsolve_sessions' not in self.data:
            self.data['total_upsolve_sessions'] = 0
            dump_flag = True
        
        if 'total_time_spent' not in self.data:
            self.data['total_time_spent'] = 0
            dump_flag = True

        if curr_date not in self.data: 
            self.data.update({
                curr_date:{
                    'total_contests_taken_today': 0,
                    'total_problems_solved_today': 0,
                    'contests': [],
                    'upsolve_sessions': []

                }
            })
            dump_flag = True

        if dump_flag: 
            with open('data.json', 'w') as handle:
                print(json.dumps(self.data, indent=4, sort_keys=True), file = handle)
            handle.close()

        self.total_contests_taken_today = self.data[curr_date]['total_contests_taken_today']
        self.total_problems_solved_today = self.data[curr_date]['total_problems_solved_today']
        return True
    
    def update_database(self, contest_info):
        curr_date = strftime("%d-%m-%Y", gmtime())
        if contest_info['event_type'] == "contest":
            del contest_info['event_type']
            self.data[curr_date]['contests'].append(contest_info)
            self.data['total_contests_attended'] += 1
            self.data[curr_date]['total_contests_taken_today'] = self.total_contests_taken_today + 1
        else:
            del contest_info['event_type']
            self.data[curr_date]['upsolve_sessions'].append(contest_info)
            self.data['total_upsolve_sessions'] += 1
        self.data[curr_date]['total_problems_solved_today'] = self.total_problems_solved_today + contest_info['problems_solved']
        self.data['total_problems_solved'] += contest_info['problems_solved']
        self.data['total_time_spent'] += int(contest_info['contest_duration'])

        with open('data.json', 'w') as handle:
            print(json.dumps(self.data, indent=4, sort_keys=True), file = handle)
        handle.close()
        self.load_data()

    def save_data(self, contest_info, contest_duration):
        print("Thanks for taking the contest. Please provide feedback")
        end_time = strftime("%H:%M:%S", gmtime())
        problems_solved = int(input("Problems_solved: "))
        rating = int(input("Rate Difficulty (1 - 10): "))
        contest_info.update(
            {
                'end_time': end_time,
                'problems_solved': problems_solved,
                'rating': rating,
                'contest_duration': contest_duration,
            }
        )
        self.load_data()
        self.update_database(contest_info) 
        print("Great! We have saved your data.\nYou can also do upsolving sessions "
        "using 'upsolve' command or quit using 'quit' command.")

    def get_contest_start_info(self, parsed_command):
        duration = self.default_duration[parsed_command[0]]
        problems = self.default_problems[parsed_command[0]]
        if len(parsed_command) > 1:
            duration = parsed_command[1]
        if len(parsed_command) > 2:
            problems = parsed_command[2]
        start_date = strftime("%d-%m-%Y", gmtime())
        start_time = strftime("%H:%M:%S", gmtime())
        contest_info = {
            'duration': duration,
            'problems': problems,
            'start_date': start_date,
            'start_time': start_time,
        }
        return contest_info

    def contest(self, parsed_command):
        contest_info = self.get_contest_start_info(parsed_command)
        contest_info['event_type'] = parsed_command[0]
        start_time = datetime.now().replace(microsecond=0)
        flag = False
        duration = int(contest_info['duration'])
        print("Contest has started!!!!!")
        sixty_min_flag = True
        ten_min_flag = True
        thirty_min_flag = True
        while  start_time + timedelta(minutes = duration) > datetime.now():
            if duration >= 120 and start_time + timedelta(minutes = duration - 60) == datetime.now().replace(microsecond=0) and sixty_min_flag:
                print("1 hour left! SPEED UP!!")
                playsound("./media/sound_sample/notification_sound.wav")
                sixty_min_flag = False
            if start_time + timedelta(minutes = duration - 30) == datetime.now().replace(microsecond=0) and thirty_min_flag:
                print("30 mins left! BUCKLE UP!!")
                playsound("./media/sound_sample/notification_sound.wav")
                thirty_min_flag = False
            if start_time + timedelta(minutes = duration - 10) == datetime.now().replace(microsecond=0) and ten_min_flag:
                print("10 mins left! FINISH UP!!")
                playsound("./media/sound_sample/notification_sound.wav")
                ten_min_flag = False
            if keyboard.is_pressed('ESC'):
                flag = True
                contest_duration = (datetime.now() - start_time)
                contest_duration = contest_duration.total_seconds()//60
                print(f"Contest finished in {contest_duration} mins!")
                self.save_data(contest_info, contest_duration)
                break

        if flag == True: 
            return
        print("Time finished!!")
        self.save_data(contest_info, contest_info['duration'])

    def statistics(self):
        self.load_data()
        curr_date = strftime("%d-%m-%Y", gmtime())
        print("Problems solved in total are: ", self.data['total_problems_solved'])
        print("Problems left to meet daily goal: ", self.problems_goal - self.data[curr_date]['total_problems_solved_today'])
        print("Total Contests Left today: ", self.default_goal - self.data[curr_date]['total_contests_taken_today'])
        print("Avg time taken per sum: ",round(self.data['total_problems_solved']/self.data['total_time_spent'], 1), "mins")

    def start_app(self):
        while True:
            command = input()
            parsed_command = self.parse(command)

            if parsed_command[0] == "quit":
                return True

            if parsed_command[0] == "contest":
                self.contest(parsed_command)
            elif parsed_command[0] == "upsolve":
                self.contest(parsed_command)
            elif parsed_command[0] == "stats":
                self.statistics()
            else:
                print("Error!! No such command exist please try again")

        return True

    def __init__(self):
        self.default_duration = {
            'contest':120,
            'upsolve': 60,
        }
        self.default_problems = {
            'contest':6,
            'upsolve':2,
        }
        self.default_goal = 5
        self.problems_goal = 30
        self.app_starter = True
        if self.load_data():
            self.app_starter = self.start_app()
        else:
            self.app_starter = False


placement = PlacementManager()
if placement.app_starter == False:
    print("ERROR!! App did not start properly!!")