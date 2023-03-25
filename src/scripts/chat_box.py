import amino
from time import sleep

from src.utils import Chats
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor
import colorama
from colorama import init, Fore
colorama.init()

Yellow = Fore.YELLOW
Reset = Fore.RESET

		# -- chat box functions by azayakasa --
		
		
class ChatBox:
	def __init__(self, client: amino.Client, sub_client: amino.SubClient):
		self.client = client
		self.sub_client = sub_client
	
	
	def start(self):
		chat_id = Chats.chats(self.sub_client)
		try:
			print(
					f"""	
	[{Yellow}1{Reset}] Kick {Yellow}all{Reset} users from chat
	[{Yellow}2{Reset}] Clear {Yellow}chat{Reset} from messages
	[{Yellow}3{Reset}] Set view {Yellow}mode{Reset} with timer
	[{Yellow}4{Reset}] Copy {Yellow}chat{Reset}
	[{Yellow}5{Reset}] Invite {Yellow}users{Reset} to chat"""
			)
			select = int(input(f"{Yellow}Select{Reset} {Yellow}->{Reset} "))
			if select == 1:
				self.kick_all_users_from_chat(chat_id)
			elif select == 2:
				self.clear_chat_from_messages(chat_id)
			elif select == 3:
				duration = int(input(f"{Yellow}Duration{Reset} in seconds - "))
				self.set_view_mode_with_timer(chat_id, duration)
			elif select == 4:
				self.copy_chat(chat_id)
			elif select == 5:
				self.invite_users_to_chat(chat_id)

		except Exception as e:
			print(e)
	
	
	def kick_all_users_from_chat(self, chat_id: str):
		with ThreadPoolExecutor(max_workers=100) as executor:
			try:
				users_count = self.sub_client.get_chat_thread(
					chatId=chat_id).membersCount
				if users_count > 10:
					chat_users = self.sub_client.get_chat_users(
						chatId=chat_id,
						start=0,
						size=100).userId
					for user_id, nickname in zip(
						chat_users.userId, chat_users.nickname):
						if user_id != self.sub_client.profile.userId:
							print(f"{Yellow}Kicked{Reset} - {nickname}!")
							executor.submit(self.sub_client.kick, user_id, chat_id)
			except Exception as e:
				print(e)


	def clear_chat_from_messages(self, chat_id: str):
		page_token = None
		while True:
			print(f"{Yellow}Deleting{Reset} messages")
			with ThreadPoolExecutor(max_workers=100) as executor:
				try:
					messages = self.sub_client.get_chat_messages(
						chatId=chat_id,
						size=100,
						pageToken=page_token)
					page_token = messages.nextPageToken
					for message_id in messages.messageId:
						executor.submit(self.sub_client.delete_message, chat_id, message_id)
				except Exception as e:
					print(e)


	def set_view_mode_with_timer(self, chat_id: str, duration: int):
		try:
			self.sub_client.edit_chat(chatId=chat_id, viewOnly=True)
			print(f"{Yellow}Chat{Reset} mode is set to viewOnly")
			while duration > 0:
				print(f"{duration} seconds left")
				duration -= 1
				sleep(1)
			self.sub_client.edit_chat(chatId=chat_id, viewOnly=False)
			print(f"{Yellow}ViewOnly{Reset} mode is disabled")
		except Exception as e:
			print(e)


	def copy_chat(self, chat_id: str):
		try:
			chat_info = self.sub_client.get_chat_thread(
				self.client.get_from_code(
						input(f"{Yellow}Chat link{Reset} - ")
					).objectId
				).json
			title = chat_info["title"]
			content = chat_info["content"]
			icon = chat_info["icon"]
			keywords = chat_info["keywords"]
			chat_style = chat_info["extensions"]
			fans_only = chat_style["fansOnly"]
			background_image = chat_style["bm"][1]
			self.sub_client.edit_chat(
				chatId=chat_id,
				title=title,
				content=content,
				icon=icon,
				keywords=keywords,
				fansOnly=fans_only)
			print(f"{Yellow}Copied{Reset} chat")
		except Exception as e:
			print(e)
	
	
	def invite_users_to_chat(self, chat_id: str):
		while True:
			with ThreadPoolExecutor(max_workers=100) as executor:
				try:
					online_users = self.sub_client.get_online_users(start=0, size=100)
					for user_id, nickname in zip(
							online_users.profile.userId, online_users.nickname):
						print(f"{Yellow}Invited{Reset} - {nickname} to chat")
						[executor.submit(self.sub_client.invite_to_chat, user_id, chat_id)]
				except Exception as e:
					print(e)
                      
                      
		# -- chat box functions by azayakasa --

