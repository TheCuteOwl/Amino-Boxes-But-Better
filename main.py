import amino
from json import loads
from requests import get
from src.service import MainApp
import colorama
from colorama import Fore, init
import sys, subprocess, shutil
colorama.init()
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


def main():
    
	print_centered(
		f"""
[{Yellow}Authors{Reset}] {Yellow}zeviel, Fixed by TheCuteOwl{Reset}
[{Yellow}GitHub{Reset}] {Yellow}https://github.com/zeviel | https://github.com/TheCuteOwl{Reset}
""")
	try:
		MainApp().start()
	except Exception as e:
		print(e)


if __name__ == "__main__":
	main()
