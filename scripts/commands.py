import asyncio, discord, os
import colorama as col

import utils


# A test command
async def test(config: dict, message):
    await utils.send_r(message, message, f"Running v{ config['VERSION'] }")
    await message.add_reaction(config["YES_EMOJI"])


# Deletes a message by ID
async def delete(config: dict, message, message_id: int):
    delete_message = await message.channel.fetch_message(message_id)

    await message.add_reaction(config["YES_EMOJI"])
    await asyncio.sleep(0.5)
    await delete_message.delete()
    await asyncio.sleep(1)
    await message.delete()


# Deletes the last messages in a channel, amount is defined in the command
async def purge(config: dict, message, amount: int, case: int):
    try:
        if amount > config["PURGE_MAX"]:
            raise Exception("too many purge messages")

        else:
            print(f"{col.Fore.RED}[purge] {col.Style.RESET_ALL}purging {amount} messages")

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

    embed_var = discord.Embed(title = "Help Command", description = desc_text, color = config["EMBED_COLOR"])

    await utils.send_e(message, message, embed_var)
    await message.add_reaction(config["YES_EMOJI"])


# Secrete help command for stuff like role commands
async def help2(config: dict, message):
    embed_var = discord.Embed(title = "*Help* Command", description = utils.file_read(config["HELP_FILES_PATH"], "help_file_secrete.txt"), color = config["EMBED_COLOR"])

    await utils.send_e(message, message, embed_var)
    await message.add_reaction(config["YES_EMOJI"])


# Provides in depth help for a command
async def syntax_help(config: dict, message, command: str):
    try:
        embed_var = discord.Embed(title = f"Syntax Help: {command}", description = utils.file_read(config["SYNTAX_FILES_PATH"], f"{command}.txt"), color = config["EMBED_COLOR"])

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
async def status(config: dict, client, message, args: str):
    try:
        status_type = args.split("; ")[0]
        status_message = args.split("; ")[1]

        if status_type not in ["online", "dnd", "idle", "offline", "invisible"]:
            raise Exception("invalid status")

        await client.change_presence(activity = discord.Game(str(status_message)), status = discord.Status[status_type])
        await message.add_reaction(config["YES_EMOJI"])

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


# "Spams" a message (one big message)
async def spam(config: dict, message, args: str):
    try:
        spam_message = ""
        amount = int(args.split("; ")[0])
        text = args.split("; ")[1]
        print(f"{col.Fore.RED}[spam] {col.Style.RESET_ALL}spamming: {text}, {amount} times")

        if (len(text) + 1) * int(amount) >= 2000:
            raise Exception("too many spam messages")

        for _ in range(int(amount)):
            spam_message += f"{text}\n"

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
            print(f"{col.Fore.RED}[megaspam] {col.Style.RESET_ALL}spamming: {text}, {amount} times")
            await message.add_reaction(config["YES_EMOJI"])

            for i in range(amount):
                print(f"{col.Fore.RED}[megaspam] {col.Style.RESET_ALL}on message: {i + 1} of {amount}")
                await utils.send(message, text)

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


# Change your roles (hehe)
async def role(config: dict, message, args: str):
    try:
        action = args.split("; ")[0]
        role_name = args.split("; ")[1]

        if action == "add":
            member = message.author
            role = discord.utils.get(member.guild.roles, name = role_name)

            await member.add_roles(role)
            await message.add_reaction(config["YES_EMOJI"])

        elif action == "remove":
            member = message.author
            role = discord.utils.get(member.guild.roles, name = role_name)

            await member.remove_roles(role)
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

    else: await utils.send(message, "I don't wanna vc by myself...")


# Leaves a VC
async def leave(config: dict, message):
    if message.guild.voice_client:
        await message.guild.voice_client.disconnect()
        await utils.send(message, "ok")

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
                vc.play(discord.FFmpegPCMAudio(executable = config["FFMPEG_EXEC_PATH"], source = config["VC_FILES_PATH"] + name))

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
async def invite(config: dict, message):
    try:
        invite_link = await message.channel.create_invite()

        await utils.send_r(message, message, invite_link)
        await message.add_reaction(config["YES_EMOJI"])

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])


# Yes
async def hitlist(config: dict, message):
    embed_var = discord.Embed(title = "HITLIST", description = "1: Rodrigo", color = config["EMBED_COLOR"])
    await utils.send_e(message, message, embed_var)


# Adds or removes a server or channel from the specified blacklist
async def blacklist(config: dict, message, args: str):
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

            else: raise Exception("ID already in blacklist")

        elif option == "remove":
            contents = utils.file_read(config["BLACKLIST_PATH"], f"{type}.txt")
            lines = contents.split("\n")
            lines.remove(id)
            new_lines = [x + "\n" for x in lines]
            new_contents = "".join(new_lines)

            utils.file_write(config["BLACKLIST_PATH"], f"{type}.txt", new_contents)
            await message.add_reaction(config["YES_EMOJI"])

    except Exception as e:
        await utils.send_r(message, message, utils.error_handler(config, str(e)))
        await message.add_reaction(config["NO_EMOJI"])