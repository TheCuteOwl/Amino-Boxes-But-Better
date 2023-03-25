import amino

from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor
import colorama, sys, subprocess, shutil
from colorama import init, Fore
colorama.init()

		# -- activity box functions by zeviel -- 

Yellow = Fore.YELLOW
Reset = Fore.RESET
def clear_console():
    if sys.platform.startswith('win'):
        _ = subprocess.call('cls', shell=True)
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        _ = subprocess.call('clear', shell=True)
    else:
        print('Unsupported platform. Cannot clear console.')

def print_centered(text):
    console_width, _ = shutil.get_terminal_size()
    padding = (console_width - len(text)) // 2
    print(' ' * padding + text)

def input_centered(prompt):
    console_width, _ = shutil.get_terminal_size()
    prompt_lines = prompt.split('\n')
    padding = (console_width - max(len(line) for line in prompt_lines)) // 2
    centered_prompt = '\n'.join(' ' * padding + line for line in prompt_lines)
    user_input = input(centered_prompt)
    return user_input


class ActivityBox:
	def __init__(self, sub_client: amino.SubClient):
		self.sub_client = sub_client


	def start(self):
		try:
			print(
				f"""
	[{Yellow}1{Reset}] Follow online {Yellow}users{Reset}
	[{Yellow}2{Reset}] Unfollow from {Yellow}followed users{Reset}
	[{Yellow}3{Reset}] Like recent {Yellow}blogs{Reset}
	[{Yellow}4{Reset}] Play {Yellow}quizzes{Reset}
"""
			)
			select = int(input(f"[{Yellow}Select{Reset}] {Yellow}->{Reset} "))
			if select == 1:
				self.follow_online_users()
			elif select == 2:
				self.unfollow_from_followed_users()
			elif select == 3:
				self.like_recent_blogs()
			elif select == 4:
				self.play_quizzes()
		except Exception as e:
			print(e)


	def follow_online_users(self):
		followed = []
		while True:
			with ThreadPoolExecutor(max_workers=100) as executor:
				try:
					online_users = self.sub_client.get_online_users(
						start=0, size=100).profile.userId
					recent_users = self.sub_client.get_all_users(
						type="recent",
						start=0,
						size=100).profile.userId
					users = [*online_users, *recent_users]
					for user_id in followed:
						if user_id in users:
							users.remove(user_id)
					for user_id in users:
						followed.append(user_id)
						executor.submit(self.sub_client.follow, [user_id])
					print(f"Following")
				except Exception as e:
					print(e)
       
                     
	def unfollow_from_followed_users(self):
		while True:
			with ThreadPoolExecutor(max_workers=100) as executor:
				following_count = self.sub_client.get_user_info(
						userId=self.sub_client.profile.userId).followingCount
				if following_count > 0:
					followed_users = self.sub_client.get_user_following(
						userId=self.sub_client.profile.userId,
						start=0,
						size=100).userId
					for user_id in followed_users:
						executor.submit(self.sub_client.unfollow, user_id)
				print(f"{Yellow}Unfollowed{Reset} everyone")
				
				
	def like_recent_blogs(self):

		while True:
			with ThreadPoolExecutor(max_workers=100) as executor:
				recent_blogs = self.sub_client.get_recent_blogs(
					start=0, size=100).blogId
				for blog_id in recent_blogs:
					executor.submit(self.sub_client.like, blog_id)
					print(f"{Yellow}Liked{Reset} -> {Yellow}{blog_id}{Reset}")


	def play_quizzes(self):
		answers_list = []
		questions_list = []
		best_quizzes = self.sub_client.get_best_quiz(
			start=0, size=100).blogId
		for quiz_id in best_quizzes:
			is_finished = self.sub_client.get_quiz_rankings(quizId=quiz_id).profile.isFinished
			if is_finished is False:
				quiz_info = self.sub_client.get_blog_info(quizId=quiz_id).json["blog"]
				quiz_title = quiz_info["title"]
				questions = quiz_info["quizQuestionList"]
				total_questions = quiz_info["extensions"]["quizTotalQuestionCount"]
				print(f"[quiz] -> [{quiz_title}]")
				for x, question in enumerate(questions, 1):
					print(
						f"-- [quiz][{x}/{total_questions}] -> [Choosing the right answer]..."
					)
					question_id = question["quizQuestionId"]
					answers = question["extensions"]["quizQuestionOptList"]
					for answer in answers:
						answer_id = answer["optId"]
						self.sub_client.play_quiz(
							quizId=quiz_id,
							questionIdsList=[question_id],
							answerIdsList=[answer_id])
						latest_score = self.sub_client.get_quiz_rankings(
							quizId=quiz_id).profile.latestScore
						if latest_score > 0:
							print(
								f"-- [quiz][{x}/{total_questions}] -> [Answer found]!"
							)
							questions_list.append(question_id)
							answers_list.append(answer_id)
				for i in range(2):
					try:
						self.sub_client.play_quiz(
							quizId=quiz_id,
							questionIdsList=questions_list,
							answerIdsList=answers_list,
							quizMode=i)
					except Exception as e:
						print(e)
							

		# -- activity box functions by zeviel --
		
		
