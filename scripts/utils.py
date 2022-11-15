import yaml, datetime, discord, aiohttp
from dateutil import tz
import colorama as col

# changes the value of a given key in a yaml file
def update_yaml(yaml_file_name: str, key: str, value):
    with open(yaml_file_name, "r") as f:
        data = yaml.safe_load(f)

    data[key] = value

    with open(yaml_file_name, "w") as f:
        yaml.dump(data, f)

# appends a value to a given key in a yaml file
def append_yaml(yaml_file_name: str, key: str, value):
    with open(yaml_file_name, "r") as f:
        data = yaml.safe_load(f)

    data[key].append(value)

    with open(yaml_file_name, "w") as f:
        yaml.dump(data, f)

# removes a value from a given key in a yaml file
def remove_yaml(yaml_file_name: str, key: str, value):
    with open(yaml_file_name, "r") as f:
        data = yaml.safe_load(f)

    data_new = data[key]
    data[key] = data_new.remove(value)

    with open(yaml_file_name, "w") as f:
        yaml.dump(data, f)

# returns a dictionary containing config values from the config files
def config(config_path: str, token_path: str):
    with open(f"{config_path}", "r") as file:
        config = yaml.safe_load(file)

    with open(f"{token_path}", "r") as file:
        token = yaml.safe_load(file)

    TOKEN = token["token"]
    WEBHOOK_LOG = token["webhook_log"]

    BOT_ID = config["bot"]["id"]
    ADMIN_NAME = config["bot"]["admin"]["admin_name"]
    ADMIN_ID = config["bot"]["admin"]["admin_id"]
    EMBED_COLOR = config["bot"]["embed_color"]
    PLAYING_STATUS = config["bot"]["playing_status"]
    VERSION = config["bot"]["version"]
    MEGASPAM_MAX = int(config["bot"]["megaspam_max"])
    PURGE_MAX = int(config["bot"]["purge_max"])

    YES_EMOJI = config["emoji"]["yes_emoji"]
    NO_EMOJI = config["emoji"]["no_emoji"]

    LOGS_PATH = config["files"]["logs_path"]
    SNIPE_PATH = config["files"]["snipe_path"]
    IMAGES_PATH = config["files"]["images_path"]
    VC_FILES_PATH = config["files"]["vc_files_path"]
    VC_DOWNLOAD_PATH = config["files"]["vc_download_path"]
    HELP_FILES_PATH = config["files"]["help_files_path"]
    SYNTAX_FILES_PATH = config["files"]["syntax_files_path"]
    FFMPEG_EXEC_PATH = config["files"]["ffmpeg_exec_path"]
    BLACKLIST_PATH = config["files"]["blacklist_path"]

    WEBHOOK_CHANNEL = config["webhook"]["webhook_channel"]
    USE_WEBHOOK = config["webhook"]["use_webhook"]

    bl_server = file_read(BLACKLIST_PATH, "server.txt")
    bl_channel = file_read(BLACKLIST_PATH, "channel.txt")
    bl_response_server = file_read(BLACKLIST_PATH, "response_server.txt")
    bl_response_channel = file_read(BLACKLIST_PATH, "response_channel.txt")
    bl_role = file_read(BLACKLIST_PATH, "role.txt")
    bl_user = file_read(BLACKLIST_PATH, "user.txt")

    snipe_message = config["snipe_message"]

    config_dict = {
        "TOKEN": TOKEN,
        "WEBHOOK_LOG": WEBHOOK_LOG,

        "BOT_ID": BOT_ID,
        "ADMIN_NAME": ADMIN_NAME,
        "ADMIN_ID": ADMIN_ID,
        "EMBED_COLOR": EMBED_COLOR,
        "PLAYING_STATUS": PLAYING_STATUS,
        "VERSION": VERSION,
        "MEGASPAM_MAX": MEGASPAM_MAX,
        "PURGE_MAX": PURGE_MAX,

        "YES_EMOJI": YES_EMOJI,
        "NO_EMOJI": NO_EMOJI,

        "LOGS_PATH": LOGS_PATH,
        "SNIPE_PATH": SNIPE_PATH,
        "IMAGES_PATH": IMAGES_PATH,
        "VC_FILES_PATH": VC_FILES_PATH,
        "VC_DOWNLOAD_PATH": VC_DOWNLOAD_PATH,
        "HELP_FILES_PATH": HELP_FILES_PATH,
        "SYNTAX_FILES_PATH": SYNTAX_FILES_PATH,
        "FFMPEG_EXEC_PATH": FFMPEG_EXEC_PATH,
        "BLACKLIST_PATH": BLACKLIST_PATH,

        "WEBHOOK_CHANNEL": WEBHOOK_CHANNEL,
        "USE_WEBHOOK": USE_WEBHOOK,

        "bl_server": bl_server,
        "bl_channel": bl_channel,
        "bl_response_server": bl_response_server,
        "bl_response_channel": bl_response_channel,
        "bl_role": bl_role,
        "bl_user": bl_user,

        "snipe_message": snipe_message
    }

    return config_dict

# returns a datetime object with the given format
def get_date_time(type: int):
    match type:
        case 0: return datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        case 1: return datetime.datetime.now().strftime("%m-%d-%Y")
        case 2: return datetime.datetime.now().strftime("%m/%d/%Y")
        case 3: return datetime.datetime.now().strftime("%H:%M:%S")

# converts UTC time and date to local time and date
def convert_utc_time(input_time: str):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    utc = datetime.datetime.strptime(input_time.split(".")[0], '%Y-%m-%d %H:%M:%S')
    utc = utc.replace(tzinfo = from_zone)
    local_time = utc.astimezone(to_zone).replace(tzinfo = None)
    new_time = datetime.datetime.strptime(str(local_time), "%Y-%m-%d %H:%M:%S")

    return new_time.strftime('%m-%d-%Y %H:%M:%S')

# logs text to a file, if the file does not exist it will create it
def log(logs_path: str, file_name: str, text: str):
    with open(f"{logs_path}{file_name}.log", "a", encoding = "utf-8") as file:
        file.write(f"{text}\n")

# appends given text to a file of the given name
def file_append(file_path: str, file_name: str, text: str):
    with open(file_path + file_name, "a", encoding = "utf-8") as file:
        file.write(text)

# writes given text to given file, deletes what was previously there
def file_write(file_path: str, file_name: str, text: str):
    with open(file_path + file_name, "r+", encoding = "utf-8") as file:
        file.seek(0)
        file.truncate()
        file.write(text)

# reads and returns the contents of a given file
def file_read(file_path: str, file_name: str):
    with open(file_path + file_name, "r", encoding = "utf-8") as file:
        return file.read()

# takes a technical error as input and returns a simplified error message
def error_handler(config: dict, error: str):
    print(f"{col.Fore.YELLOW}>[Error Handler]: {error}")

    if error == "list index out of range":                   text = "Syntax error"
    elif error.count("invalid literal for int()") > 0:       text = "Syntax error"
    elif error.count("No such file or directory") > 0:       text = "Syntax error"
    elif error == "invalid command syntax":                  text = "Syntax error"
    elif error == "invalid status":                          text = "Status error"
    elif error == "too many megaspam messages":              text = f"Amount of messages is too high, the max is { config['MEGASPAM_MAX'] } messages"
    elif error == "too many spam messages":                  text = "Amount of messages is too high, the amount of characters times the number of messages must be fewer than 2000"
    elif error == "too many purge messages":                 text = f"Amount of messages is too high, the max is { config['PURGE_MAX'] } messages"
    elif error == "Not connected to voice channel":          text = "Not connected to voice channel"
    elif error == "Audio not paused":                        text = "Audio Error"
    elif error == "Audio not playing":                       text = "Audio Error"
    elif error == "'NoneType' object has no attribute 'id'": text = "Role error"
    elif error == "list.remove(x): x not in list":           text = "ID not in blacklist"
    elif error == "ID already in blacklist":                 text = "ID already in blacklist"

    else: text = "Unknown Error"

    return f"[Error Handler]: **{text}**\n(try `hesa help`)\n```{error}```"

# runs when the main bot loop is closed
def exit_handler(config: dict):
    import colorama as col

    print(f"{col.Fore.YELLOW}>[Exit Handler]: Closing bot.")
    log(config["LOGS_PATH"], f"LOG-{get_date_time(1)}", f">[Exit Handler]: Closing bot.")
    print(f"{col.Style.RESET_ALL}Closed")

# used for the syntax command
def syntax_embed(config: dict, command):
    return discord.Embed(title = f"Syntax Help: {command}", description = file_read(config["SYNTAX_FILES_PATH"], f"{command}.txt"), color = config["EMBED_COLOR"])

# splits a string at the nth occurrence of a char
def split_nth(string: str, split_char: str, nth_occurrence: int):
    temp = string.split(split_char)
    res = split_char.join(temp[:nth_occurrence]), split_char.join(temp[nth_occurrence:])
    return res

# Logs a message to the logs webhook 
async def webhook_log(config: dict, webhook_message: str):
    async with aiohttp.ClientSession() as client_session:
        webhook = discord.Webhook.from_url(config["WEBHOOK_LOG"], adapter=discord.AsyncWebhookAdapter(client_session))
        await webhook.send(content=webhook_message)


# --== Discord stuff ==-- #

# sends a message to the channel of the provided message object
async def send(message, text: str):
    await message.channel.send(text)

# sends a message to the channel of the provided message object that is a reply to another message
async def send_r(message, ref, text: str):
    await message.channel.send(text, reference = ref)

# sends an embed message to the channel of the provided message object
async def send_e(message, ref, emb):
     await message.channel.send(embed = emb, reference = ref)