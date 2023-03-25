import amino

from src.utils import Chats
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor
import colorama
from colorama import Fore, init
colorama.init()
import sys, subprocess, shutil

Yellow = Fore.YELLOW
Reset = Fore.RESET

		# -- raid box functions by zeviel --
def print_centered(text):
    console_width, _ = shutil.get_terminal_size()
    padding = (console_width - len(text)) // 2
    print(' ' * padding + text)


class RaidBox:
	def __init__(self, client: amino.Client, sub_client: amino.SubClient):
		self.client = client
		self.sub_client = sub_client


	def start(self):

		try:
			print_centered(f"""
	[{Yellow}1{Reset}] Spam wall with {Yellow}comments{Reset}
	[{Yellow}2{Reset}] Spam blog with {Yellow}comments{Reset}
	[{Yellow}3{Reset}] Spam chat with {Yellow}messages{Reset}
	[{Yellow}4{Reset}] Kick user from {Yellow}chat{Reset}
	[{Yellow}5{Reset}] Spam public chats with {Yellow}message{Reset}
	[{Yellow}6{Reset}] Spam with {Yellow}blogs{Reset}
	[{Yellow}7{Reset}] Spam with {Yellow}wikis{Reset}
"""
			)
			select = int(input(f"[{Yellow}Select{Reset}] -> "))
			if select == 1:
				self.spam_wall_with_comments()
			elif select == 2:
				self.spam_blog_with_comments()
			elif select == 3:
				self.spam_chat_with_messages()
			elif select == 4:
				self.kick_user_from_chat()
			elif select == 5:
				self.spam_public_chats_with_message()
			elif select == 6:
				self.spam_with_blogs()
			elif select == 7:
				self.spam_with_wikis()
		except Exception as e:
			print(e)


	def spam_wall_with_comments(self):
		user_id = self.client.get_from_code(input("[User link] ->")).objectId
		message = input("[Message] -> ")
		for i in range(int(input("[Comments count] -> "))):
			self.sub_client.comment(message=message, userId=user_id)
			print(f"[{i+1}][Comment is sent]...")
	
	
	def spam_blog_with_comments(self):

		import time

		blog_id = self.client.get_from_code(input("[Blog link] ->")).objectId
		message = input("[Message] -> ")
		for i in range(int(input("[Comments count] -> "))):
			time.sleep(1)
			self.sub_client.comment(message=message, blogId=blog_id)
			print(f"[{i+1}][Comment is sent]...")
	
	
	def spam_chat_with_messages(self):
		chat_id = Chats.chats(self.sub_client)
		message = input("[Message] -> ")
		message_type = int(input("[Message type] -> "))
		while True:
			print("[Spamming!]")
			with ThreadPoolExecutor(max_workers=100) as executor:
				[executor.submit(self.sub_client.send_message,
					chat_id,
					message,
					message_type) for _ in range(100_000_000)]
	
	
	def kick_user_from_chat(self):
		chat_id = Chats.chats(self.sub_client)
		while True:
			try:
				user_id = self.client.get_from_code(input("-- [User link] ->")).objectId
				self.sub_client.kick(chatId=chat_id, userId=user_id)
				print("[Kicked user from chat!]")
			except Exception as e:
				print(e)


	def spam_public_chats_with_message(self):
		message = input("[Message] -> ")
		message_type = int(input("[Message type] -> "))
		with ThreadPoolExecutor(max_workers=100) as executor:
			try:
				public_chats = self.sub_client.get_public_chat_threads(size=100)
				for chat_id, title in zip(public_chats.chatId, public_chats.title):
					print(f"[Joined into] -> [{title}]")
					[executor.submit(self.sub_client.join_chat, chat_id) for _ in range(2)]
					[executor.submit(
						self.sub_client.send_message,
						chat_id,
						message,
						message_type) for _ in range(15)]
					print(f"[Spammed messages in] -> [{title}]")
				print("[All public chats is spammed successfully!]")
			except Exception as e:
				print(e)
		
	
	def spam_with_blogs(self):
		title = input("[Title] -> ")
		content = input("[Content] -> ")
		while True:
			try:
				self.sub_client.post_blog(title=title, content=content)
			except Exception as e:
				print(e)


	def spam_with_wikis(self):
		title = input("[Title] -> ")
		content = input("[Content] -> ")
		while True:
			try:
				self.sub_client.post_wiki(title=title, content=content)
			except Exception as e:
				print(e)
			
			
		# -- raid box functions by zeviel --
