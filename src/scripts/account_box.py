import amino

from tabulate import tabulate
import sys, subprocess, shutil
import colorama
from colorama import init, Fore
		# -- account box functions by morphine & morirarti --

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

Yellow = Fore.YELLOW
class AccountBox:
	def __init__(self, client: amino.Client):
		self.client = client





	def start(self):

		try:
			print(f"""

	[{Yellow}1{Reset}] Get {Yellow}account{Reset} info
	[{Yellow}2{Reset}] Get {Yellow}blocker{Reset} users
	[{Yellow}3{Reset}] Get {Yellow}blocked{Reset} users
""")
			select = int(input(f"{Yellow}Select{Reset} {Yellow}->{Reset} "))
			if select == 1:
				self.get_account_info()
			elif select == 2:
				self.get_blocker_users()
			elif select == 3:
				self.get_blocked_users()
		except Exception as e:
			print(e)
	
	
	def get_account_info(self):
		account_info = self.client.get_account_info().json
		email = account_info["email"]
		user_id = account_info["uid"]
		phone_number = account_info["phoneNumber"]
		amino_id = account_info["aminoId"]
		created_time = account_info["createdTime"]
		print(
			f"""
email - {Yellow}{email}{Reset}
userId - {Yellow}{user_id}{Reset}
phoneNumber - {Yellow}{phone_number}{Reset}
aminoId - {Yellow}{amino_id}{Reset}
createdTime - {Yellow}{created_time}{Reset}
"""
	)
		input(f'{Yellow}Press{Reset} Any {Yellow}Key{Reset} To go at the previous menu')


	def get_blocker_users(self):
		try:
			blocker_users = self.client.get_blocker_users(
				start=0, size=100)
			for user_id in blocker_users:
				nickname = self.client.get_user_info(userId=user_id).nickname
				print(
					f"userId - {Yellow}{user_id}{Reset} - nickname - {Yellow}{nickname}{Reset}"
				)
		except Exception as e:
			print(e)


	def get_blocked_users(self):
		try:
			blocked_users = self.client.get_blocked_users(
				start=0, size=100)
			for user_id, nickname in zip(
					blocked_users.userId, blocked_users.nickname):
				print(
					f"userId - {Yellow}{user_id} - nickname - {Yellow}{nickname}"
				)
		except Exception as e:
			print(e)
	
		
		
		
