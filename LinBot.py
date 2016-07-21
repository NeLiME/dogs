#!/usr/bin/env python3
import discord
import random
import os
import asyncio

import logging
logging.basicConfig(level=logging.INFO)

def rand_file(path):
	return path + "/" + random.choice([x for x in os.listdir(path) if os.path.isfile(path + "/" + x)])

class LinBot(discord.Client):
	def __init__(self):
		super().__init__()
		self.player = None
		self.voice = None
	
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		print('------')
		for server in self.servers:
			if self.is_voice_connected(server):
				print("Found existing voice connection. Joining")
				self.voice = self.voice_client_in()
		#print("Starting random color thingy")
		#asyncio.get_event_loop().create_task(self.rainbowz())

	async def rainbowz(self):
		while not self.is_closed:
			color = None
			for server in self.servers:
				for role in server.roles:
					if role.name == "Rainbowz":
						color = discord.Color(random.randint(0x000000, 0xFFFFFF))
						print("Color: " + str(color))
						await self.edit_role(server, role, color=color)
			if color == None:
				await asyncio.sleep(60)
			await asyncio.sleep(.7)

	def do_leave(self):
		print("do_leave()")
	
	async def join_voice(self, message):
		voice_ch = message.author.voice_channel
		if voice_ch is None:
			await self.send_message(message.channel, 'Dafuq? Ur not in a voice chat idiot!')
			print("ERROR: Not in voice chat")
		else:
			if self.voice is None:
				self.voice = await self.join_voice_channel(voice_ch)
			elif self.voice.channel != voice_ch:
				await self.leave_voice()
				self.voice = await self.join_voice_channel(voice_ch)
				if self.player != None:
					self.player.stop()
			print("Connecting voice")
			return self.voice is not None

	async def leave_voice(self):
		print(self.voice)
		await self.voice.disconnect()
		print("Disconnecting voice")

	async def on_message(self, message):
		if message.author == self.user:
			return
		
		if message.content.startswith('!peter'):
			await send_message(message.channel, msg)
		
		elif message.content.startswith('!RIP'):
			if await self.join_voice(message):
				await self.send_message(message.channel, ':poop:')
				print("Playing grace.mp3")
				self.player = self.voice.create_ffmpeg_player('grace.mp3')
				self.player.start()
		elif message.content.startswith('!coinflip'):
			state = bool(random.getrandbits(1))
			if state:
				await self.send_message(message.channel, ':flag_us:')
			else:
				await self.send_message(message.channel, ':flag_ru:')
		elif message.content.startswith('!thomas'):
			if await self.join_voice(message):
				await self.send_message(message.channel, ':poop:')
				print("Playing thomas.mp3")
				self.player = self.voice.create_ffmpeg_player('thomas.mp3', after=self.do_leave)
				self.player.start()
		
		elif message.content.startswith('!fart'):
			if await self.join_voice(message):
				await self.send_message(message.channel, ':poop:')
				sound = rand_file("fart")
				print("Playing " + sound)
				global player
				self.player = self.voice.create_ffmpeg_player(sound)
				self.player.start()
		
		elif message.content.startswith('!shadap') or message.content.startswith('!stfu'):
			self.player.stop()
			self.player = None
	
		elif message.content.startswith('!die'):
			self.voice = self.voice_client_in(message.server)
			if self.voice is None:
				await self.send_message(message.channel, 'I\'m not in a voice chat stuped!')
			else:
				if self.player:
					self.player.stop()
					self.player = None
				await self.leave_voice()
				await self.send_message(message.channel, ':robot: :gun:')

bot = LinBot()
bot.run('---API-KEY-HERE---')
