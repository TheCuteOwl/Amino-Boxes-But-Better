import amino

from src.utils import Chats
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor
import colorama
from colorama import init, Fore
Yellow = Fore.YELLOW
Reset = Fore.RESET
		
		# -- other box functions by auroraflow & roger --
		

class OtherBox:
	def __init__(self, client: amino.Client, sub_client: amino.SubClient):
		self.client = client
		self.sub_client = sub_client


	def start(self):

		try:
			print(
				f"""
	[{Yellow}1{Reset}] Send {Yellow}system{Reset} message
	[{Yellow}2{Reset}] Get {Yellow}community{Reset} info
	[{Yellow}3{Reset}] Check in all {Yellow}communities{Reset}"""
			)
			select = int(input(f"{Yellow}Select{Reset} = "))
			if select == 1:
				self.send_system_message()
			elif select == 2:
				self.get_community_info()
			elif select == 3:
				self.check_in_all_communities()

		except Exception as e:
			print(e)


	def send_system_message(self):
		chat_id = Chats.chats(self.sub_client)
		while True:
			try:
				self.sub_client.send_message(
					chatId=chat_id,
					message=input(f"{Yellow}Message{Reset} - "),
					messageType=int(input(f"{Yellow}Message{Reset} type - ")))
				print(f"{Yellow}Message{Reset} is sent!")
			except Exception as e:
				print(e)


	def get_community_info(self):
		com_id = self.client.get_from_code(
				input(f"{Yellow}Community{Reset} link = ")).json["extensions"]["community"]["ndcId"]
		community_info = self.client.get_community_info(comId=com_id).json
		icon = community_info["icon"]
		tagline = community_info["tagline"]
		endpoint = community_info["endpoint"]
		content = community_info["content"]
		created_time = community_info["createdTime"]
		community_cover = str(community_info["promotionalMediaList"]).split("'")[1]
		print(
			f"""
{Yellow}Community{Reset} icon link = {Yellow}{icon}{Reset}
{Yellow}Community{Reset} cover link = {Yellow}{community_cover}{Reset}
{Yellow}Community{Reset} tagline = {Yellow}{tagline}{Reset}
{Yellow}Community{Reset} endpoint = {Yellow}{endpoint}{Reset}
{Yellow}Community {Reset}created time = {Yellow}{created_time}{Reset}
"""
	)


	def check_in_all_communities(self):
		try:
			clients = self.client.sub_clients(start=0, size=100).comId
			with ThreadPoolExecutor(max_workers=100) as executor:
				for com_id in clients:
					self.sub_client = amino.SubClient(
						comId=com_id, profile=self.client.profile)
					executor.submit(
						self.sub_client.check_in,
						self.sub_client.lottery)
				print(f"{Yellow}Checked{Reset} in all communities!")
		except Exception as e:
			print(e)
	
	
		# -- other box functions by auroraflow & roger --
	
	
