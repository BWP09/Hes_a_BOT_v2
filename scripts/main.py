import nextcord, atexit, random, asyncio, os, aiohttp
import colorama as col

import utils, commands


def update_config():
    global CONFIG
    CONFIG = utils.config("C:/Users/BWP09/Desktop/Code/Python/Discord/Bots/Hes_a_BOT_v2/config/config.yml")


update_config()
col.init()
atexit.register(utils.exit_handler, CONFIG)
intents = nextcord.Intents.all()
client = nextcord.Client(intents = intents)


@client.event
async def on_ready():
    print(f"{col.Style.RESET_ALL}Logged in as:")
    print(f"{client.user} (v{ CONFIG['VERSION'] })")
    await client.change_presence(status = nextcord.Status.online)
    await client.change_presence(activity = nextcord.Game(CONFIG['PLAYING_STATUS']))


@client.event
async def on_message_edit(before, after):
    update_config()

    before_message = str(before.content)
    after_message = str(after.content)

    username = str(before.author).split("#")[0]
    channel = str(before.channel)
    channel_id = int(before.channel.id)
    server = str(before.guild)

    if CONFIG["USE_WEBHOOK"]:
        if channel_id == CONFIG["WEBHOOK_CHANNEL"]: return

        utils.webhook_log(CONFIG, f"*[MESSAGE EDIT]:* **[{utils.get_date_time(0)}]: [{server}: {channel}]: __{username}:__**\n**>OLD:** {before_message}\n**>NEW:** {after_message}\n")

    utils.log(CONFIG["LOGS_PATH"], f"LOG-{utils.get_date_time(1)}", f"[MESSAGE EDIT]: [{utils.get_date_time(0)}]: [{server}: {channel}]: {username}:\n>OLD: {before_message}\n>NEW: {after_message}\n")
    print(f"{col.Fore.RED}[MESSAGE EDIT]: {col.Fore.LIGHTMAGENTA_EX}[{utils.get_date_time(0)}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.CYAN}{username}:\n{col.Fore.LIGHTBLUE_EX}>OLD: {before_message}\n>NEW: {col.Fore.LIGHTBLUE_EX}\033[4m{after_message}\033[0m")


@client.event
async def on_message_delete(message):
    update_config()

    user_message = str(message.content)

    username = str(message.author).split("#")[0]
    channel = str(message.channel)
    channel_id = int(message.channel.id)
    server = str(message.guild)

    if CONFIG["USE_WEBHOOK"]:
        if channel_id == CONFIG["WEBHOOK_CHANNEL"]: return

        utils.webhook_log(CONFIG, f"*[MESSAGE DELETE]:* **[{utils.get_date_time(0)}]: [{server}: {channel}]: __{username}:__** {user_message}")

    utils.update_yaml(CONFIG["SNIPE_MESSAGE_PATH"], "snipe_message", f"[{utils.get_date_time(0)}]: [{server}: {channel}]: {username}: {user_message}")

    utils.log(CONFIG["LOGS_PATH"], f"LOG-{utils.get_date_time(1)}", f"[MESSAGE DELETE]: [{utils.get_date_time(0)}]: [{server}: {channel}]: {username}: {user_message}")
    utils.log(CONFIG["SNIPE_PATH"], f"SNIPE-{utils.get_date_time(1)}", f"[{utils.get_date_time(0)}]: [{server}: {channel}]: {username}: {user_message}")
    print(f"{col.Fore.RED}[MESSAGE DELETE]: {col.Fore.LIGHTMAGENTA_EX}[{utils.get_date_time(0)}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.CYAN}{username}: {col.Fore.LIGHTBLUE_EX}\033[4m{user_message}\033[0m")


@client.event
async def on_message(message):
    update_config()

    user_message = str(message.content).lower()
    user_message_default = str(message.content)

    username = str(message.author).split("#")[0]
    author = str(message.author)
    author_id = int(message.author.id)
    channel = str(message.channel)
    channel_id = int(message.channel.id)
    server = str(message.guild)

    if CONFIG["USE_WEBHOOK"]:
        if channel_id == CONFIG["WEBHOOK_CHANNEL"]: return

    try: server_id = int(message.guild.id)
    except: server_id = 0

    bl = 0

    # checks if the the message is a reply to another, if it is then it will re-log the original message and the new reply
    if message.reference != None:
        ref_message = await message.channel.fetch_message(message.reference.message_id)

        ref_content = str(ref_message.content)
        ref_username = str(ref_message.author).split("#")[0]
        ref_message_time = utils.convert_utc_time(str(ref_message.created_at))

        if CONFIG["USE_WEBHOOK"]:
            utils.webhook_log(CONFIG, f"*=>* **[{ref_message_time}]: [{server}: {channel}]: __{ref_username}:__** {ref_content}\n^ **[{utils.get_date_time(0)}]: [{server}: {channel}]: __{username}:__** {user_message_default}")

        utils.log(CONFIG["LOGS_PATH"], f"LOG-{utils.get_date_time(1)}", f"=>[{ref_message_time}]: [{server}: {channel}]: {ref_username}: {ref_content}\n^ [{utils.get_date_time(0)}]: [{server}: {channel}]: {username}: {user_message_default}")
        print(f"{col.Fore.YELLOW}=>{col.Fore.LIGHTMAGENTA_EX}[{ref_message_time}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.CYAN}{ref_username}: {col.Fore.LIGHTBLUE_EX}{ref_content}\n{col.Fore.YELLOW}^ {col.Fore.LIGHTMAGENTA_EX}[{utils.get_date_time(0)}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.CYAN}{username}: {col.Fore.LIGHTBLUE_EX}{user_message_default}")

    else:
        if CONFIG["USE_WEBHOOK"]:
            utils.webhook_log(CONFIG, f"**[{utils.get_date_time(0)}]: [{server}: {channel}]: __{username}:__** {user_message_default}")

        utils.log(CONFIG["LOGS_PATH"], f"LOG-{utils.get_date_time(1)}", f"[{utils.get_date_time(0)}]: [{server}: {channel}]: {username}: {user_message_default}")
        print(f"{col.Fore.LIGHTMAGENTA_EX}[{utils.get_date_time(0)}]: {col.Fore.GREEN}[{server}: {col.Fore.LIGHTGREEN_EX}{channel}{col.Fore.GREEN}]: {col.Fore.CYAN}{username}: {col.Fore.LIGHTBLUE_EX}{user_message_default}")


    if author_id == CONFIG["BOT_ID"]: return

    elif user_message.count("(!)") > 0: return

    elif str(CONFIG["bl_server"]).count(str(server_id)) > 0: bl = 1
    elif str(CONFIG["bl_channel"]).count(str(channel_id)) > 0: bl = 1
    elif str(CONFIG["bl_user"]).count(str(author_id)) > 0: bl = 1
    if user_message.count("blacklist") > 0: bl = 0

    #--== Commands ==--#

    if user_message.startswith("!") and bl != 1: # !p<AMOUNT> !d<MESSAGE_ID>
        command = user_message[1]
        args = int(user_message.removeprefix(f"!{command}"))

        if command == "p": await commands.purge(CONFIG, message, args, 0)

        elif command == "d": await commands.delete(CONFIG, message, args)


    elif user_message.startswith("hesa") and bl != 1:
        try:
            command = user_message.split(" ")[1]
            args = utils.split_nth(user_message_default, " ", 2)[1]

        except Exception as e:
            await utils.send_r(message, message, utils.error_handler(CONFIG, str(e)))
            return

        if command == "blacklist": await commands.blacklist(CONFIG, message, args)

        elif command == "test": await commands.test(CONFIG, message)

        elif command == "purge": await commands.purge(CONFIG, message, int(args), 1)

        elif command == "help": await commands.help(CONFIG, message)

        elif command == "*help*": await commands.help2(CONFIG, message)

        elif command == "syntax": await commands.syntax_help(CONFIG, message, args)

        elif command == "id": await commands.id(CONFIG, message, args)

        elif command == "status": await commands.status(CONFIG, client, message, args)

        elif command == "spam": await commands.spam(CONFIG, message, args)

        elif command == "megaspam": await commands.megaspam(CONFIG, message, args)

        elif command == "role": await commands.role(CONFIG, client, message, args)

        elif command == "snipe": await commands.snipe(CONFIG, message)

        elif command == "invite": await commands.invite(CONFIG, message)

        elif command == "hitlist": await commands.hitlist(CONFIG, message)


        elif command == "join": await commands.join(CONFIG, message)

        elif command == "leave": await commands.leave(CONFIG, message)

        elif command == "vc": await commands.vc(CONFIG, message, args)
        
        
        elif command == "run": await commands.py(CONFIG, message, args)

        else: await utils.invalid_command(CONFIG, message, command)


    elif str(CONFIG["bl_response_server"]).count(str(server_id)) > 0: return
    elif str(CONFIG["bl_response_channel"]).count(str(channel_id)) > 0: return
    elif bl == 1: return

    #--== Responses ==--#

    elif user_message.count("hassan") > 0:
        await message.channel.send("kidnapped your family + L + ratio + bozo", file = nextcord.File(CONFIG["IMAGES_PATH"] + "hassan_bozo.jpg"))

    elif user_message.count("jack") > 0:
        await message.channel.send("did someone say jack....\n", file = nextcord.File(CONFIG["IMAGES_PATH"] + "jackhigh.png"), reference = message)


    elif user_message == "ok" or user_message == "okay":
        await utils.send(message, "ok then")

    elif user_message == "yeah":
        await utils.send(message, "yeah")

    elif user_message == "big sad":
        await utils.send(message, ":cry:")

    elif user_message == "no":
        await utils.send(message, "how about yes")

    elif user_message.count("dumb") > 0:
        await utils.send(message, "you're dumb")

    elif user_message.count("jk") > 0:
        await utils.send(message, "i dont think so :thinking:")


    elif user_message == "why":
        rand_int = random.randint(0, 1)
        match rand_int:
            case 0: await utils.send_r(message, message, "because yes")
            case 1: await utils.send_r(message, message, "why not?")

    elif user_message == "yes":
        rand_int = random.randint(0, 2)
        match rand_int:
            case 0: await utils.send(message, "sure")
            case 1: await utils.send(message, "ok")
            case 2: await utils.send(message, "fur sure...")

    elif user_message.count("lol") > 0:
        rand_int = random.randint(0, 1)
        match rand_int:
            case 0: await utils.send_r(message, message, "omg so lol")
            case 1: await utils.send_r(message, message, "lol")


client.run(CONFIG["TOKEN"])