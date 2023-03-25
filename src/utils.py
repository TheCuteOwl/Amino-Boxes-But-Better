import amino

from tabulate import tabulate
import amino
import secmail
import colorama
from colorama import Fore, init
import sys, subprocess, shutil
colorama.init()

Yellow = Fore.YELLOW
Reset = Fore.RESET
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
	


class Login:
	@staticmethod
	def login(client: amino.Client):
		while True:
			colorama.init()
			try:
				print(
					f"""
					[{Yellow}1{Reset}] Login with {Yellow}email{Reset} & {Yellow}password{Reset}
					[{Yellow}2{Reset}] Login with {Yellow}sid{Reset}
					[{Yellow}3{Reset}] Generate an {Yellow}Amino{Reset} Account
                        """)
				select = int(input_centered(f"[{Yellow}Select{Reset}] {Yellow}->{Reset}  "))
				if select == 1:
					email = input(f"[{Yellow}Email{Reset}] -> ")
					password = input(f"[{Yellow}Password{Reset}] -> ")
					client.login(email=email, password=password)
					clear_console()
					break
				elif select == 2:
					SID = input(f"[{Yellow}SID{Reset}] {Yellow}->{Reset} ")
					client.login_sid(SID=SID)
					clear_console()
					break
				elif select == 3:
					clear_console()
					from generator import generator
					generator()
			except:
				print(f'{Fore.RED}Error, retry please{Reset}')
				clear_console()

			


class Communities:
	@staticmethod
	def communities(client: amino.Client):
		while True:
			try:
				clients = client.sub_clients(start=0, size=100)
				for x, name in enumerate(clients.name, 1):
					print_centered(f"{Yellow}{x}{Reset} - {name}")

				return clients.comId[int(input_centered(f"[{Yellow}Select the community{Reset}] ->{Reset} ")) - 1]
			except Exception as e:
				print(e)
				clear_console()
			clear_console()

class Chats:
	@staticmethod
	def chats(sub_client: amino.SubClient):
		while True:
			try:
				chats = sub_client.get_chat_threads(start=0, size=100)
				for z, title in enumerate(chats.title, 1):
					print_centered(f"{Yellow}{z}{Reset} - {Yellow}{title}{Reset}")
				return chats.chatId[int(input_centered(f"[{Yellow}Select the chat{Reset}] ->{Reset} ")) - 1]
			except Exception as e:
				print(e)
				clear_console()

			clear_console()