import asyncio, nextcord, os
import colorama as col

import utils


# TODO MAKE LOGGING BETTER



# A test command
async def test(config: dict, message):
    await utils.send_r(message, message, f"Running v{ config['VERSION'] }")
    await message.add_reaction(config["YES_EMOJI"])


# Deletes a message by ID
async def delete(config: dict, message: nextcord.Message, message_id: int):
    delete_message = await message.channel.fetch_message(message_id)

    await message.add_reaction(config["YES_EMOJI"])
    await asyncio.sleep(0.25)
    await delete_message.delete()
    await asyncio.sleep(0.5)
    await message.delete()

    print(f'{col.Fore.LIGHTRED_EX}[delete] {col.Style.RESET_ALL}deleted "{delete_message.content}"')


# Deletes the last messages in a channel, amount is defined in the command
async def purge(config: dict, message, amount: int, case: int):
    try:
        if amount > config["PURGE_MAX"]:
            raise Exception("too many purge messages")

        else:
            print(f"{col.Fore.LIGHTRED_EX}[purge] {col.Style.RESET_ALL}purging {amount} messages")

            await message.add_reaction(config["YES_EMOJI"])
            await asyncio.sleep(1)

            async for delete_message in message.channel.history(limit = amount + 1):
                await delete_message.delete()
                await asyncio.sleep(0.1)

            if case == 1:
                await utils.send(message, f"Purge Complete :smiling_imp:\nDeleted {amount} messages")

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


# The help command
async def help(config: dict, message):
    original_desc_text = utils.file_read(config["HELP_FILES_PATH"], "help_file.txt")
    desc_text = utils.var_parser(original_desc_text, ["VERSION", "ADMIN_NAME", "GITHUB_LINK"], [config["VERSION"], config["ADMIN_NAME"], config["GITHUB_LINK"]])

    embed_var = nextcord.Embed(title = "Help Command", description = desc_text, color = config["EMBED_COLOR"])

    await utils.send_e(message, message, embed_var)
    await message.add_reaction(config["YES_EMOJI"])


# Secrete help command for stuff like role commands
async def help2(config: dict, message):
    embed_var = nextcord.Embed(title = "*Help* Command", description = utils.file_read(config["HELP_FILES_PATH"], "help_file_secrete.txt"), color = config["EMBED_COLOR"])

    await utils.send_e(message, message, embed_var)
    await message.add_reaction(config["YES_EMOJI"])


# Provides in depth help for a command
async def syntax_help(config: dict, message, command: str):
    try:
        embed_var = nextcord.Embed(title = f"Syntax Help: {command}", description = utils.file_read(config["SYNTAX_FILES_PATH"], f"{command}.txt"), color = config["EMBED_COLOR"])

        await utils.send_e(message, message, embed_var)
        await message.add_reaction(config["YES_EMOJI"])

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


# Sends the ID of the specified object
async def id(config: dict, message, args: str):
    try:
        try: server_id = message.guild.id
        except: server_id = 0

        if args == "server":
            await utils.send_r(message, message, f"Current server's ID: {server_id}")

        elif args == "channel":
            await utils.send_r(message, message, f"Current channel's ID: {message.channel.id}")

        elif args.startswith("<@"):
            user_id = args.removeprefix("<@").removesuffix(">")
            await utils.send_r(message, message, f"User's ID: {user_id}")

        else: raise Exception("invalid command syntax")

        await message.add_reaction(config["YES_EMOJI"])

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


# Changes the status of the bot
async def status(config: dict, client: nextcord.Client, message, args: str):
    try:
        status_type = args.split("; ")[0]
        status_message = args.split("; ")[1]

        if status_type not in ["online", "dnd", "idle", "offline", "invisible"]:
            raise Exception("invalid status")

        await client.change_presence(activity = nextcord.Game(str(status_message)), status = nextcord.Status[status_type])
        await message.add_reaction(config["YES_EMOJI"])

        print(f'{col.Fore.LIGHTRED_EX}[status] {col.Style.RESET_ALL}changed to "\033[4m{status_type}\033[0m" playing "\033[4m{status_message}\033[0m"')

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


# "Spams" a message (one big message)
async def spam(config: dict, message, args: str):
    try:
        spam_message = ""
        amount = int(args.split("; ")[0])
        text = args.split("; ")[1]

        if (len(text) + 1) * int(amount) >= 2000:
            raise Exception("too many spam messages")

        for _ in range(int(amount)):
            spam_message += f"{text}\n"

        print(f'{col.Fore.LIGHTRED_EX}[spam] {col.Style.RESET_ALL}spamming "\033[4m{text}\033[0m", {amount} times')
        
        await utils.send(message, spam_message)
        await message.add_reaction(config["YES_EMOJI"])

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


# Spams a message (actual)
async def megaspam(config: dict, message, args: str):
    try:
        amount = int(args.split("; ")[0])
        text = args.split("; ")[1]

        if amount > config["MEGASPAM_MAX"]:
            raise Exception("too many megaspam messages")

        else:
            print(f'{col.Fore.LIGHTRED_EX}[megaspam] {col.Style.RESET_ALL}spamming: "\033[4m{text}\033[0m", {amount} times')
            await message.add_reaction(config["YES_EMOJI"])

            for i in range(amount):
                print(f"{col.Fore.LIGHTRED_EX}[megaspam] {col.Style.RESET_ALL}on message: {i + 1} of {amount}")
                await utils.send(message, text)

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


# Change your roles (hehe)
async def role(config: dict, client: nextcord.Client, message, args: str):
    try:
        action = args.split("; ")[0]
        server_id = args.split("; ")[1]
        user_id = args.split("; ")[2]
        role_id = args.split("; ")[3]
        
        server = await client.fetch_guild(int(server_id))
        user = await server.fetch_member(int(user_id))
        role = server.get_role(int(role_id))

        if action == "add":
            await user.add_roles(role) # type: ignore
            print(f"{col.Fore.LIGHTRED_EX}[role] {col.Style.RESET_ALL}added \033[4m{role}\033[0m to \033[4m{user}\033[0m in \033[4m{server}\033[0m")

        elif action == "remove":
            await user.remove_roles(role) # type: ignore
            print(f"{col.Fore.LIGHTRED_EX}[role] {col.Style.RESET_ALL}removed \033[4m{role}\033[0m from \033[4m{user}\033[0m in \033[4m{server}\033[0m")
        
        await message.add_reaction(config["YES_EMOJI"])

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


# Sends the last deleted message
async def snipe(config: dict, message):
    await utils.send(message, f"[Last deleted message]: {config['snipe_message']}")
    await message.add_reaction(config["YES_EMOJI"])


# Joins a VC
async def join(config: dict, message):
    if message.author.voice:
        channel = message.author.voice.channel
        await channel.connect()
        await utils.send(message, "sure")

        print(f"{col.Fore.LIGHTRED_EX}[vc] {col.Style.RESET_ALL}joined \033[4m{channel.name}\033[0m in \033[4m{channel.guild}\033[0m")

    else: await utils.send(message, "I don't wanna vc by myself...")


# Leaves a VC
async def leave(config: dict, message):
    if message.guild.voice_client:
        await message.guild.voice_client.disconnect()
        await utils.send(message, "ok")

        print(f"{col.Fore.LIGHTRED_EX}[vc] {col.Style.RESET_ALL}left a vc in \033[4m{message.guild}\033[0m")

    else: await utils.send(message, "I'm not even in a vc")


# Has many smaller commands, used to play audio in a VC
async def vc(config: dict, message, args: str): # hesa vc play; melvin.mp4
    try:
        try:
            option = args.split("; ")[0]
            name = args.split("; ")[1]

        except:
            option = args
            name = ""


        if option == "play":
            if message.guild.voice_client:
                vc = message.guild.voice_client
                vc.play(nextcord.FFmpegPCMAudio(executable = config["FFMPEG_EXEC_PATH"], source = config["VC_FILES_PATH"] + name))

                print(f'{col.Fore.LIGHTRED_EX}[vc] {col.Style.RESET_ALL}playing "\033[4m{name}\033[0m" in \033[4m{vc.channel}\033[0m in \033[4m{message.guild}\033[0m')

            else: raise Exception("Not connected to voice channel")

        elif option == "stop":
            if message.guild.voice_client:
                vc = message.guild.voice_client
                vc.stop()

            else: raise Exception("Not connected to voice channel")

        elif option == "pause":
            if message.guild.voice_client:
                vc = message.guild.voice_client
                if vc.is_playing():
                    vc.pause()

                else: raise Exception("Audio not playing")
            else: raise Exception("Not connected to voice channel")

        elif option == "resume":
            if message.guild.voice_client:
                vc = message.guild.voice_client
                if vc.is_paused:
                    vc.resume()

                else: raise Exception("Audio not paused")
            else: raise Exception("Not connected to voice channel")

        elif option == "list":
            names = "Files:\n"
            files = os.listdir(config["VC_FILES_PATH"])

            for file in files:
                names += file + "\n"

            await utils.send_r(message, message, names)

        # elif option == "search":
        #     link = search_youtube(name)
        #     await message.channel.send(f"Found video... now downloading", reference = message)

        #     file_name = download_youtube(link)

        #     if message.guild.voice_client:
        #         vc = message.guild.voice_client
        #         vc.play(discord.FFmpegPCMAudio(executable = FFMPEG_EXEC_PATH, source = file_name))
        #         await message.channel.send(f"playing file...", reference = message)

        #     else: await message.channel.send("done!", reference = message)

        else: raise Exception("invalid command syntax")

        await message.add_reaction(config["YES_EMOJI"])

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


# Sends an invite to the server you are in
async def invite(config: dict, client, message, args):
    try:
        channel = await client.fetch_channel(int(args))

        invite_link = await channel.create_invite()

        print(f'{col.Fore.LIGHTRED_EX}[invite] {col.Style.RESET_ALL}\033[4m{message.author}\033[0m created an invite link: "\033[4m{invite_link}\033[0m"')

        await utils.send_r(message, message, invite_link)
        await message.add_reaction(config["YES_EMOJI"])

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


# Yes
async def hitlist(config: dict, message):
    embed_var = nextcord.Embed(title = "HITLIST", description = "1: Rodrigo", color = config["EMBED_COLOR"])
    await utils.send_e(message, message, embed_var)


# Adds or removes a server or channel from the specified blacklist
async def blacklist(config: dict, message, args: str):
    if message.author.id != config["ADMIN_ID"]: return
    
    try:
        option = args.split("; ")[0]
        type = args.split("; ")[1].split(": ")[0]
        id = args.split("; ")[1].split(": ")[1]

        if option == "add":
            contents = utils.file_read(config["BLACKLIST_PATH"], f"{type}.txt")
            lines = contents.split("\n")

            if id not in lines:
                utils.file_append(config["BLACKLIST_PATH"], f"{type}.txt", f"{id}\n")
                await message.add_reaction(config["YES_EMOJI"])

                print(f"{col.Fore.LIGHTRED_EX}[blacklist] {col.Style.RESET_ALL}blacklisted {type} \033[4m{id}\033[0m")

            else: raise Exception("ID already in blacklist")

        elif option == "remove":
            contents = utils.file_read(config["BLACKLIST_PATH"], f"{type}.txt")
            lines = contents.split("\n")
            lines.remove(id)
            new_lines = [x + "\n" for x in lines]
            new_contents = "".join(new_lines)

            utils.file_write(config["BLACKLIST_PATH"], f"{type}.txt", new_contents)
            await message.add_reaction(config["YES_EMOJI"])

            print(f"{col.Fore.LIGHTRED_EX}[blacklist] {col.Style.RESET_ALL}un-blacklisted {type} \033[4m{id}\033[0m")

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


async def unban(config: dict, client, message, args: str):
    try:
        guild_id = int(args.split("; ")[0])
        user_id = int(args.split("; ")[1])

        guild = await client.fetch_guild(guild_id)
        user: nextcord.User = await client.fetch_user(user_id)

        print(f'{col.Fore.LIGHTRED_EX}[unban] {col.Style.RESET_ALL}\033[4m{message.author}\033[0m has unbanned "\033[4m{user.name}\033[0m"')

        await guild.unban(user)
        await message.add_reaction(config["YES_EMOJI"])

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


async def list_servers(config: dict, client, message, args: str):
    try:
        guilds = client.guilds

        text = ""
        for guild in guilds:
            text += f"{guild.name}, {guild.id}\n"
        
        await utils.send_r(message, message, text)
        await message.add_reaction(config["YES_EMOJI"])

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


async def list_server_channels(config: dict, client, message, args: str):
    try:
        guild_id = int(args)

        text = ""
        for guild in client.guilds:
            if guild.id == guild_id:
                for channel in guild.text_channels:
                    text += f"{channel.name}, {channel.id}\n"
        
        await utils.send_r(message, message, text)
        await message.add_reaction(config["YES_EMOJI"])

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])