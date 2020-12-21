import discord
from discord.utils import get
#import Ai
import random
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
import numpy as np

token = 'NzU3ODI3NjM0NTE1NDEwOTg5.X2mD-w.UdtNVnnCa8AFWNb7mVXPlJGXMPs'
intents = discord.Intents.all()
client = discord.Client(intents=intents)

#----------------------------------COLORS-----------------------------------
colors_dict = {'red' : 0xff0000 , 'green' : 0x00ff00 , 'blue' : 0x00bbff , 'purple' : 0x9400D3,
			   'cyan' : 0x00fffd, 'orange':0xffaa00 , 'pink' : 0xff00ff ,  'yellow': 0xffff00,
			   'lime': 0x44ff00 , 'brown' : 0xd35400,'black':0x010101, 'gold':0xffd700}

colors_list =['red','green','blue','purple',
			  'cyan','orange','pink','yellow',
			  'lime','brown','black','gold']	

#-----------------------LIST OF COMMANDS------------------------------------
command_list = ['info','announce(mods only)','activity','color','say','coin','dice']
help_string = ''
for com in command_list:
	help_string += '`'
	help_string += com
	help_string += '` '

#-------------------------MembersList Data----------------------------------
df = pd.read_csv('Discord_member_activity.csv')
df['Sr.No'] = range(len(df))
df.set_index('Sr.No' , inplace =True)


# method expected by client. This runs once when connected



@client.event
async def on_message(msg):
	#-------------------Get Members list-----------------
	'''guild = client.get_guild(750745174996418703)
	members_list = guild.members
	mem_val = []
	for m in members_list:
		mem_val.append(m.name)
	d = {'Name' : mem_val , 'Messages' : np.zeros(49)}
	df = pd.DataFrame(d)
	df.to_csv('Discord_member_activity.csv' , index=False)'''



	if msg.author.bot:
		return


	guild = client.get_guild(750745174996418703)
	message = msg.content.lower().strip()
	channel = msg.channel

	aarya = client.get_user(578942888755593217)
	aarya_role = get(msg.author.guild.roles , name='.꧁༺Aarya༻꧂')
	random_color = random.choice(colors_list)
	try:
		await aarya_role.edit(colour = discord.Colour(int(colors_dict[random_color])))
	except:
		pass

	#-----------------------------Add ACTIVITY DATA--------------------
	if msg.guild == guild:
		
		row = df[df['Name'] == msg.author.name]
		row_n = row.index
		print(row)
		row_n = row_n[0]
		df.loc[row_n, 'Messages'] += 1
		df.to_csv('Discord_member_activity.csv' , index=False)
		prev_author = msg.author.name
		print(df)
		
	#----------------------------Scan Messages-----------------------------------
	if 'pls rob' in message:
		await channel.send("__**NO ROBBING!!!**__")

	if msg.author.name =='Dyno':
		await channel.send("Fuck you Dyno!")
	#--------------------------COMMANDS----------------------------------------
	if message[:6] == 'dhanos':

		msg_parts = message.split()
		if len(msg_parts) == 1:
			await channel.send("Hello Human")
			return
		else:
			command = msg_parts[1]

		if command == 'info':
			await channel.send("I am DhanOS, your personal discord BOT :) --- created by Aarya")
		#------------------------------------SHOW ACTIVITY----------------------
		elif command == 'activity':
			acv_df = df.sort_values(by=['Messages'], ascending=False)
			acv_df = acv_df.iloc[:6 , :]
			fig, ax = plt.subplots()
			ax.barh(acv_df['Name'] ,acv_df['Messages']  )
			ax.set_yticks(acv_df['Name'])
			ax.invert_yaxis()
			ax.set_title("The chart of lifelessness")
			fig.set_figwidth(13)
			plt.savefig('Activity_graph.png')	
			file = discord.File('Activity_graph.png')
			await channel.send(file=file)

		#-----------------------------CHANGE COLOR------------------------------
		elif command == 'color' or command == 'colour':
			try:
				color = msg_parts[2]
			except:
				await channel.send("Enter a Color!!!")
				return
			name = msg.author.nick
			current_roles	= msg.author.roles
			if color in colors_list:	
				for r in current_roles:
					if name == r.name:
						new_color = int(f'{colors_dict[color]}')
						if msg_parts[3] == 'darken':
							try:
								n = int(msg_parts[4])
							except:
								n = 1
							for i in range(n):
								if new_color > 65793:
									new_color -= 65793

						await r.edit(colour = discord.Colour(new_color))
						return
				await msg.guild.create_role(name =f'{name}' , colour = discord.Colour(int(f'{colors_dict[color]}')))
				role = get(msg.author.guild.roles, name=f'{name}')
				mod_role = get(msg.author.guild.roles , name='Members')
				await role.edit(position=20)
				await msg.author.add_roles(role)
				await channel.send(f"sucessfully changed color of {name} to {color} color")
			else:
				await channel.send("Incorrect color!!!")

		#---------------------------OTHER SMALL COMMANDS-------------------------
		elif command =='coin':
			dec = random.choice([0,1])
			if dec == 1:
				await channel.send('Heads')
			else:
				await channel.send('Tails')

		elif command =='dice':
			dec = random.choice([1,2,3,4,5,6])
			await channel.send(str(dec))

		elif command == 'help':
			await channel.send(f'{help_string}')

		elif command == 'opinion':
			await channel.send('WhiteHat.JR mere jhaate pe')

		elif command == 'say':
			sentance = message[11:]
			await channel.send(sentance)
			await msg.delete()

		elif command == 'spam' and msg.author.name == 'Blunderer':
			for i in range(10):
				await channel.send("@everyone")

		#------------------------------ANNOUNCE------------------
		elif command == 'announce':
			content = message[16:]
						
			
			await channel.send(f'''📢 __**ANNOUNCEMENT**__ 

**Hello __@everyone__**,

{content}

					   							--- __***{msg.author.nick}***__''')
			await msg.delete()

		else:
			await channel.send("https://cdn.discordapp.com/attachments/757939759774564434/763001126387712000/trigger.gif")
			await channel.send("Wrong command!!")

@client.event
async def on_disconnect():
	try:
		df.to_csv('Discord_member_activity.csv' , index=False)
	except:
		pass

client.run(token)



