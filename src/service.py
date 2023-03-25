import amino
from tabulate import tabulate

from src.utils import Login
from src.utils import Communities
from src.utils import Chats
from src.scripts.raid_box import RaidBox
from src.scripts.activity_box import ActivityBox
from src.scripts.profile_box import ProfileBox
from src.scripts.chat_box import ChatBox
from src.scripts.other_box import OtherBox
from src.scripts.account_box import AccountBox
import shutil, subprocess, sys
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

def clear_console():
    if sys.platform.startswith('win'):
        _ = subprocess.call('cls', shell=True)
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        _ = subprocess.call('clear', shell=True)
    else:
        print('Unsupported platform. Cannot clear console.')

import colorama
from colorama import init, Fore
colorama.init()


class MainApp:

	def start(self):
		Yellow = Fore.YELLOW
		Reset = Fore.RESET
		self.client = amino.Client()
		Login.login(self.client)
		self.sub_client = amino.SubClient(
			comId=Communities.communities(
			self.client), profile=self.client.profile)
		while True:
			clear_console()
			try:
				print(f'''
	[{Yellow}1{Reset}] Raid Box By {Yellow}zeviel{Reset}
	[{Yellow}2{Reset}] Activity Box By {Yellow}zeviel{Reset}
	[{Yellow}3{Reset}] Profile Box By {Yellow}Savier{Reset}
	[{Yellow}4{Reset}] Chat Box By {Yellow}Azayakasa{Reset}
	[{Yellow}5{Reset}] Other Box By {Yellow}Auroraflow{Reset} & {Yellow}Roger{Reset}
	[{Yellow}6{Reset}] Account Box By {Yellow}Morphine{Reset} & {Yellow}Moriarti{Reset}
	''')
				select = int(input_centered(f"[{Yellow}Select{Reset}] {Yellow}->{Reset} "))
				if select == 1:
					clear_console()
					RaidBox(self.client, self.sub_client).start()
				elif select == 2:
					clear_console()
					ActivityBox(self.sub_client).start()
				elif select == 3:
					clear_console()
					ProfileBox(self.client, self.sub_client).start()
				elif select == 4:
					clear_console()
					ChatBox(self.client, self.sub_client).start()
				elif select == 5:
					clear_console()
					OtherBox(self.client, self.sub_client).start()
				elif select == 6:
					clear_console()
					AccountBox(self.client).start()
			except Exception as e:
				clear_console()
				print(e)