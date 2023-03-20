import os
import time, datetime
import ntplib
import json
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice,create_option
#import youtube_dl
#import pafy
#import ffmpeg
import asyncio
import random
from dotenv import dotenv_values

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageColor
import requests
import sqlite3

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 

try:
    temp_time = ntplib.NTPClient()
    response = temp_time.request('pool.ntp.org')
    x = datetime.datetime.fromtimestamp(response.tx_time)
    print('Internet date and time:',x.strftime("%d/%m/%Y  %I:%M:%S %p"))
    
except:
    print("Date Time server not Available")


client = commands.Bot(command_prefix='+', activity=discord.Game(name="/help"))
slash = SlashCommand(client,sync_commands=True)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord Server\n')
    for guild in client.guilds:
        print("Server Name:",guild.name,"  Server ID:",guild.id,'\n')
    
@slash.slash(name="ping",description="Checks voice channel ping",guild_ids= client.guilds)
async def ping(ctx:SlashContext):
    if ctx.voice_client is None:
        return await ctx.send("Im not connected to any voice channel")
    
    if ctx.voice_client is not None:
        if ctx.author.voice.channel.id == ctx.voice_client.channel.id:
            if ctx.voice_client.is_playing():
                return await ctx.send("Ping: "+str(1000 * round(ctx.guild.voice_client.average_latency,3))+"ms")
            else:
                return await ctx.send("Cant check ping if nothing is playing")
        else:
            return await ctx.send("You are not in the same voice channel as me")

@slash.slash(name="getuser",description="Get user ID",options=[create_option(name="user",description="Select a user",required=True,option_type=6)])
async def getuser(ctx:SlashContext, user:str):
    if ctx.author.guild_permissions.administrator == True:
        return await ctx.send(user.id)
    await ctx.send("You dont have the permission to use this.")
    
@slash.slash(name="toss",description="Tosses a coin",guild_ids= client.guilds)       
async def toss(ctx:SlashContext):
    coin = random.randint(1, 2)
    if coin == 1:
        return await ctx.send("Heads")
    else:
        return await ctx.send("Tails")
    
@slash.slash(name="tictactoe",description="Play TicTacToe with a fren :)",guild_ids=client.guilds,options=[create_option(name="player",description="Select player 2",required=True,option_type=6)]) 
async def tictactoe(ctx:SlashContext, player:str):
    
    if(player == ctx.author):
        return await ctx.send(f'You played against yourself. Wait, you cant do that', hidden=True)

    circle = '⭕'
    cross  = '❌'
    
    value=[':black_square_button:',':black_square_button:',':black_square_button:',':black_square_button:',':black_square_button:',':black_square_button:',':black_square_button:',':black_square_button:',':black_square_button:']
    
    z1 = await ctx.send(f'{ctx.author.mention} has challenged {player.mention} in TicTacToe')
    z2 = await ctx.send(f'Do you want to accept the challenge {player.nick} (y/n) ?')
    
    
    def check_1(m):                                                                     #Challenge Input
        if (m.content == "y" or m.content == "Y") and m.channel == ctx.channel and m.author == player:
            return m.content
            
        elif (m.content == "n" or m.content == "N") and m.channel == ctx.channel and m.author == player:
            return m.content
        
    def check_2(m):                                                                     #TOSS INPUT
        if m.content == '1' and m.channel == ctx.channel and m.author == ctx.author:
            return m.content
            
        elif m.content == '2' and m.channel == ctx.channel and m.author == ctx.author:
            return m.content

    def check_3(m):
        if m.content.isdecimal() is True:
            temp = int(m.content)
            if (temp >= 1 and temp <= 9) and m.channel == ctx.channel and m.author == first_player and value[temp - 1] == ':black_square_button:':
                
                value[temp -1] = circle
                return m.content
    
    def check_4(m):
        if m.content.isdecimal() is True:
            temp = int(m.content)
            if (temp >= 1 and temp <= 9) and m.channel == ctx.channel and m.author == second_player and value[temp - 1] == ':black_square_button:':
                
                value[temp -1] = cross
                return m.content

    def check_winner(turn):
        if turn <= 8:
            if(value[0]==value[1]==value[2]==circle) or (value[0]==value[1]==value[2]==cross):  #Hort 1
                if(value[0]==value[1]==value[2]==circle):
                    return 1
                else:
                    return 2
                
            if(value[3]==value[4]==value[5]==circle) or (value[3]==value[4]==value[5]==cross):   #Hort 2
                if(value[3]==value[4]==value[5]==circle):
                    return 1
                else:
                    return 2

            if(value[6]==value[7]==value[8]==circle) or (value[6]==value[7]==value[8]==cross):   #Hort 3
                if(value[6]==value[7]==value[8]==circle):
                    return 1
                else:
                    return 2
            
            if(value[0]==value[3]==value[6]==circle) or (value[0]==value[3]==value[6]==cross):   #Vert 1
                if(value[0]==value[3]==value[6]==circle):
                    return 1
                else:
                    return 2
            if(value[1]==value[4]==value[7]==circle) or (value[1]==value[4]==value[7]==cross):   #Vert 2
                if(value[1]==value[4]==value[7]==circle):
                    return 1
                else:
                    return 2
            if(value[2]==value[5]==value[8]==circle) or (value[2]==value[5]==value[8]==cross):   #Vert 3
                if(value[2]==value[5]==value[8]==circle):
                    return 1
                else:
                    return 2
            
            if(value[0]==value[4]==value[8]==circle) or (value[0]==value[4]==value[8]==cross):   #Diag 1
                if(value[0]==value[4]==value[8]==circle):
                    return 1
                else:
                    return 2
                
            if(value[2]==value[4]==value[6]==circle) or (value[2]==value[4]==value[6]==cross):    #Diag 2
                if(value[2]==value[4]==value[6]==circle):
                    return 1
                else:
                    return 2
        if turn >= 9:
            return 3

    try:
        msg = await client.wait_for("message",timeout=30.0 ,check=check_1)
    
    except asyncio.TimeoutError:
        await ctx.send(f'{player.nick} never responded')
        return await z2.delete()
    
    if(msg.content == "y" or msg.content == "Y"):
        await z2.edit(content="Challenge Accepted")
        await msg.delete()
        
        try:
            z3 = await ctx.send(f'{ctx.author.nick} pick ->\n1 for Heads \n2 for Tails')
            z4 = await client.wait_for("message",timeout=30.0 ,check=check_2)
            
            coin = random.randint(1, 2)
            
            if coin == 1:
                first_player = ctx.author
                second_player = player
            
            else:
                first_player = player
                second_player = ctx.author
                
            await z2.delete()
            await z3.edit(content=f'First player is : {first_player.nick} & Second Player is : {second_player.nick}')   
            await z4.delete()
            
            row = await ctx.send(f'{value[0]} {value[1]} {value[2]} \n{value[3]} {value[4]} {value[5]} \n{value[6]} {value[7]} {value[8]}')

            try:  # 1
                z5 = await ctx.send(f'{first_player.nick} , Enter valid position number(1-9)')
                z6 = await client.wait_for("message",timeout=30.0 ,check=check_3)
                
                await row.edit(content=f'{value[0]} {value[1]} {value[2]} \n{value[3]} {value[4]} {value[5]} \n{value[6]} {value[7]} {value[8]}' )
                
                winner = check_winner(1)
                
                if winner == 1:
                    await ctx.send(f'Winner is {first_player.nick}')
                    await z5.delete()
                    return await z6.delete()
                
                await z5.delete()
                await z6.delete()
                
            except asyncio.TimeoutError:
                await ctx.send(f'{first_player.nick} never responded')
                return await z5.delete()
            
            
            try:  # 2
                z5 = await ctx.send(f'{second_player.nick} , Enter valid position number(1-9)')
                z6 = await client.wait_for("message",timeout=30.0 ,check=check_4)
                
                await row.edit(content=f'{value[0]} {value[1]} {value[2]} \n{value[3]} {value[4]} {value[5]} \n{value[6]} {value[7]} {value[8]}' )
                
                winner = check_winner(2)
                
                if winner == 2:
                    await ctx.send(f'Winner is {second_player.nick}')
                    await z5.delete()
                    return await z6.delete()
                
                await z5.delete()
                await z6.delete()
                
            except asyncio.TimeoutError:
                await ctx.send(f'{second_player.nick} never responded')
                return await z5.delete()
            
            try:  # 3
                z5 = await ctx.send(f'{first_player.nick} , Enter valid position number(1-9)')
                z6 = await client.wait_for("message",timeout=30.0 ,check=check_3)
                
                await row.edit(content=f'{value[0]} {value[1]} {value[2]} \n{value[3]} {value[4]} {value[5]} \n{value[6]} {value[7]} {value[8]}' )
                
                winner = check_winner(3)
                
                if winner == 1:
                    await ctx.send(f'Winner is {first_player.nick}')
                    await z5.delete()
                    return await z6.delete()
                
                await z5.delete()
                await z6.delete()
                
            except asyncio.TimeoutError:
                await ctx.send(f'{first_player.nick} never responded')
                return await z5.delete()
            
            try:  # 4
                z5 = await ctx.send(f'{second_player.nick} , Enter valid position number(1-9)')
                z6 = await client.wait_for("message",timeout=30.0 ,check=check_4)
                
                await row.edit(content=f'{value[0]} {value[1]} {value[2]} \n{value[3]} {value[4]} {value[5]} \n{value[6]} {value[7]} {value[8]}' )
                
                winner = check_winner(4)
                
                if winner == 2:
                    await ctx.send(f'Winner is {second_player.nick}')
                    await z5.delete()
                    return await z6.delete()
                
                await z5.delete()
                await z6.delete()
                
            except asyncio.TimeoutError:
                await ctx.send(f'{second_player.nick} never responded')
                return await z5.delete()
            
            try:  # 5
                z5 = await ctx.send(f'{first_player.nick} , Enter valid position number(1-9)')
                z6 = await client.wait_for("message",timeout=30.0 ,check=check_3)
                
                await row.edit(content=f'{value[0]} {value[1]} {value[2]} \n{value[3]} {value[4]} {value[5]} \n{value[6]} {value[7]} {value[8]}' )
                
                winner = check_winner(5)
                
                if winner == 1:
                    await ctx.send(f'Winner is {first_player.nick}')
                    await z5.delete()
                    return await z6.delete()
                
                await z5.delete()
                await z6.delete()
                
            except asyncio.TimeoutError:
                await ctx.send(f'{first_player.nick} never responded')
                return await z5.delete()
            
            try:  # 6
                z5 = await ctx.send(f'{second_player.nick} , Enter valid position number(1-9)')
                z6 = await client.wait_for("message",timeout=30.0 ,check=check_4)
                
                await row.edit(content=f'{value[0]} {value[1]} {value[2]} \n{value[3]} {value[4]} {value[5]} \n{value[6]} {value[7]} {value[8]}' )
                
                winner = check_winner(6)
                
                if winner == 2:
                    await ctx.send(f'Winner is {second_player.nick}')
                    await z5.delete()
                    return await z6.delete()
                
                await z5.delete()
                await z6.delete()
                
            except asyncio.TimeoutError:
                await ctx.send(f'{second_player.nick} never responded')
                return await z5.delete()
            
            try:  # 7
                z5 = await ctx.send(f'{first_player.nick} , Enter valid position number(1-9)')
                z6 = await client.wait_for("message",timeout=30.0 ,check=check_3)
                
                await row.edit(content=f'{value[0]} {value[1]} {value[2]} \n{value[3]} {value[4]} {value[5]} \n{value[6]} {value[7]} {value[8]}' )
                
                winner = check_winner(7)
                
                if winner == 1:
                    await ctx.send(f'Winner is {first_player.nick}')
                    await z5.delete()
                    return await z6.delete()
                
                await z5.delete()
                await z6.delete()
                
            except asyncio.TimeoutError:
                await ctx.send(f'{first_player.nick} never responded')
                return await z5.delete()
            
            try:  # 8
                z5 = await ctx.send(f'{second_player.nick} , Enter valid position number(1-9)')
                z6 = await client.wait_for("message",timeout=30.0 ,check=check_4)
                
                await row.edit(content=f'{value[0]} {value[1]} {value[2]} \n{value[3]} {value[4]} {value[5]} \n{value[6]} {value[7]} {value[8]}' )
                
                winner = check_winner(8)
                
                if winner == 2:
                    await ctx.send(f'Winner is {second_player.nick}')
                    await z5.delete()
                    return await z6.delete()
                
                await z5.delete()
                await z6.delete()
                
            except asyncio.TimeoutError:
                await ctx.send(f'{second_player.nick} never responded')
                return await z5.delete()
            
            try:  # 9
                z5 = await ctx.send(f'{first_player.nick} , Enter valid position number(1-9)')
                z6 = await client.wait_for("message",timeout=30.0 ,check=check_3)
                
                await row.edit(content=f'{value[0]} {value[1]} {value[2]} \n{value[3]} {value[4]} {value[5]} \n{value[6]} {value[7]} {value[8]}' )
                
                winner = check_winner(9)
                
                if winner == 3:
                    await ctx.send(f'Its a draw')
                    await z5.delete()
                    return await z6.delete()
                
                await z5.delete()
                await z6.delete()
                
            except asyncio.TimeoutError:
                await ctx.send(f'{first_player.nick} never responded')
                return await z5.delete()          
            
            return await row.edit(content=f'{value[0]} {value[1]} {value[2]} \n{value[3]} {value[4]} {value[5]} \n{value[6]} {value[7]} {value[8]}' )        
        
        except asyncio.TimeoutError:
            await ctx.send(f'{player.nick} never responded')
            await z2.delete()
            return await z3.delete()
    
    if(msg.content == "n" or msg.content == "N"):
        await z2.edit(content="Challenge Rejected")
        return await msg.delete()
    
@slash.slash(name="profile",description="Your Profile",guild_ids= client.guilds,options=[create_option(name="user",description="Select a user",required=True,option_type=6)])
async def profile(ctx:SlashContext, user:str):
    
    con = sqlite3.connect("C:\\Users\\SHUBHOJIT\\Desktop\\Bot\\db\\user.db")
    
    cursor = con.execute('SELECT ID,BG,color1,color2,color3,XP from PROFILE_DATA_BASIC where ID = '+str(user.id))
    
    row = 0
    for row in cursor:
        continue
    
    try:
        if user.id == row[0]:
            
            x1 = await ctx.send("Gimme a second, finding your profile card.")
            
            bg = Image.open(requests.get('https://i.imgur.com/'+str(row[1]), stream=True).raw)
            black_circle = Image.open(requests.get('https://i.imgur.com/rwI7hCE.png', stream=True).raw)
            avatar = Image.open(requests.get(user.avatar_url, stream=True).raw)
   
            black_circle = black_circle.resize((109,109))
            
            width, height = bg.size
            
            bg = bg.crop((width/2-400,height/2-300,width/2+400,height/2+300))
            draw = ImageDraw.Draw(bg, "RGBA")
            draw.rectangle(((0, 0), (800, 150)), fill=(row[2],row[3], row[4], 127))
            
            bg1 = bg.copy()
            bg1.paste(black_circle, (5,31), black_circle)
    
            avatar = avatar.resize((80,80))   
    
            mask = Image.new("L", avatar.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, 80, 80), fill=255)
    
            bg1.paste(avatar,(19,45), mask)
    
            I1 = ImageDraw.Draw(bg1)
            I1.text((115, 56), str(user.nick), font=ImageFont.truetype('C:\\Users\\SHUBHOJIT\\Desktop\\Bot\\Font\\LEMONMILK-Light.otf', 26), fill =(0, 0, 0),stroke_width=1)
            I1.text((115, 88), str(user), font=ImageFont.truetype('C:\\Users\\SHUBHOJIT\\Desktop\\Bot\\Font\\helvetica_light.ttf', 20), fill =(0, 0, 0)) 
            
            bg1.save(f"Temp_{user.id}.png")
            await x1.edit(content="", file=discord.File(f"Temp_{user.id}.png"))
            os.remove(f"Temp_{user.id}.png")
              
    except:
        x2 = await ctx.send("Profile Doesn't Exist, Making one") 
        temp1 = con.execute('SELECT BG,color1,color2,color3 from PROFILE_DATA_DEFAULT')
            
        for r in temp1:
            continue
 
        con.execute("INSERT INTO PROFILE_DATA_BASIC (ID,BG,color1,color2,color3,XP) VALUES(?, ?, ?, ?, ?, 0)",(user.id,r[0],r[1],r[2],r[3]))
        con.commit()
        
        cursor = con.execute('SELECT ID,BG,color1,color2,color3,XP from PROFILE_DATA_BASIC where ID = '+str(user.id))
        row =0
        for row in cursor:
            continue
        
        bg = Image.open(requests.get('https://i.imgur.com/'+str(row[1]), stream=True).raw)
        black_circle = Image.open(requests.get('https://i.imgur.com/rwI7hCE.png', stream=True).raw)
        avatar = Image.open(requests.get(user.avatar_url, stream=True).raw)
   
        black_circle = black_circle.resize((109,109)) 
            
        width ,height = bg.size
        
        bg = bg.crop((width/2-400,height/2-300,width/2+400,height/2+300))
        draw = ImageDraw.Draw(bg, "RGBA")
        draw.rectangle(((0, 0), (800, 150)), fill=(row[2],row[3], row[4], 127))
            
        bg1 = bg.copy()
        bg1.paste(black_circle, (5,31), black_circle)
    
        avatar = avatar.resize((80,80))   
    
        mask = Image.new("L", avatar.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 80, 80), fill=255)
    
        bg1.paste(avatar,(19,45), mask)
    
        I1 = ImageDraw.Draw(bg1)
        I1.text((115, 56), str(user.nick), font=ImageFont.truetype('C:\\Users\\SHUBHOJIT\\Desktop\\Bot\\Font\\LEMONMILK-Light.otf', 26), fill =(0, 0, 0),stroke_width=1)
        I1.text((115, 88), str(user), font=ImageFont.truetype('C:\\Users\\SHUBHOJIT\\Desktop\\Bot\\Font\\helvetica_light.ttf', 20), fill =(0, 0, 0)) 
                
        bg1.save(f"Temp_{user.id}.png")
        await x2.edit(content="", file=discord.File(f"Temp_{user.id}.png"))
        os.remove(f"Temp_{user.id}.png")
        
    con.close()
    
@slash.slash(name="change_background",description="Chnage Profile Background",guild_ids= client.guilds, options=[create_option(name="image",description="Background Image Link(Imgur Link Only)",required=True,option_type=3)])
async def change_background(ctx:SlashContext, image:str): 
                
    con1 = sqlite3.connect("C:\\Users\\SHUBHOJIT\\Desktop\\Bot\\db\\user.db")
    cursor = con1.execute('SELECT ID,BG from PROFILE_DATA_BASIC where ID ='+str(ctx.author.id))
    
    row = 0
    for row in cursor:
        continue
    
    if ctx.author.id == row[0]:
        if 'https://i.imgur.com/' == image[0:20]:
            image = image[20:]
            if image[-4:] == '.jpg' or image[-4:] == '.png':
                con1.execute("UPDATE PROFILE_DATA_BASIC set BG=? where ID=?",(image,str(ctx.author.id)))
                con1.commit()
                await ctx.send("Background Updated")
            
            elif image[-5:] == '.jpeg':
                con1.execute("UPDATE PROFILE_DATA_BASIC set BG=? where ID=?",(image,str(ctx.author.id)))
                con1.commit()
                await ctx.send("Background Updated")
                
            else:
                await ctx.send("Image format's other than jpg, jpeg, png arent supported")
        else:
            await ctx.send("Give direct image link such as *https://i.imgur.com/example.png*")
    else:
        await ctx.send("Your profile doesn't exist, create one by using /profile")
     
    con1.close()
    
@slash.slash(name="change_highlight",description="Chnage Profile Highlight",guild_ids= client.guilds, options=[create_option(name="color",description="HEX value only",required=True,option_type=3)])
async def change_highlight(ctx:SlashContext, color:str): 
                
    con1 = sqlite3.connect("C:\\Users\\SHUBHOJIT\\Desktop\\Bot\\db\\user.db")
    cursor = con1.execute('SELECT ID from PROFILE_DATA_BASIC where ID ='+str(ctx.author.id))
    
    row = 0
    for row in cursor:
        continue
    
    if ctx.author.id == row[0]:
        if color[0:1] == '#':
            if len(color) == 7:
                color = color.upper()
                color = ImageColor.getcolor(color, "RGB")
                con1.execute("UPDATE PROFILE_DATA_BASIC set color1=?,color2=?,color3=? where ID=?",(color[0],color[1],color[2],str(ctx.author.id)))
                con1.commit()
                await ctx.send("Color Updated")
                
            else:
                await ctx.send("This is not proper HEX format")
        else:
            await ctx.send("Give color in HEX format")
    else:
        await ctx.send("Your profile doesn't exist, create one by using /profile")
     
    con1.close()

@slash.slash(name="help",description="List all Commands",guild_ids= client.guilds)
async def help(ctx:SlashContext):
    
    embed = discord.Embed(title="List of commands", description="", colour=discord.Colour.magenta())
    embed.set_thumbnail(url=f'https://i.imgur.com/VvkFzOA.png')
    embed.add_field(name="Music Commands", value="play (song name/link): Play the song\npause : Pause current song\nresume: Resume playing song\nqueue : Check queued songs\nskip : Skip current song\nstop : Leaves and clear queue", inline=True)
    embed.add_field(name="Utilities", value="setup : Run this command upon inviting this bot\nhelp : List all commands\nping : Current Ping\ngetuser : Show Member's ID ", inline=True)
    embed.add_field(name="Games", value="tictactoe : Play tic tac toe(2 player)\ntoss : Toss a coin", inline=False)
    embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by: "+str(ctx.author))
    await ctx.send(embed=embed)
    
@slash.slash(name="setup",description="Run initial Setup",guild_ids= client.guilds)
async def setup(ctx:SlashContext):
    await ctx.send("Successfully Completed Initial Setup")

@slash.slash(name="test",description="This is just a test",options=[create_option(name="user",description="Select a user",required=True,option_type=6)])
async def test(ctx:SlashContext, user:str):
    return
    

client.run(dotenv_values("token.env")["BOT_TOKEN"])