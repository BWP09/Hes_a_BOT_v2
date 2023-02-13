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
def config(config_path: str):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    SECRETS_PATH = config["files"]["secrets_path_yml"]
    SNIPE_MESSAGE_PATH = config["files"]["snipe_path_yml"]

    with open(SECRETS_PATH, "r") as file:
        secrets = yaml.safe_load(file)

    with open(SNIPE_MESSAGE_PATH, "r") as file:
        snipe_message_yml = yaml.safe_load(file)


    BLACKLIST_PATH = config["files"]["blacklist_path"]

    return {
        "TOKEN": secrets["token"],
        "WEBHOOK_URL": secrets["webhook_url"],

        "GITHUB_LINK": config["bot"]["github"],

        "BOT_ID": config["bot"]["id"],
        "ADMIN_NAME": config["bot"]["admin"]["admin_name"],
        "ADMIN_ID": config["bot"]["admin"]["admin_id"],
        "EMBED_COLOR": config["bot"]["embed_color"],
        "PLAYING_STATUS": config["bot"]["playing_status"],
        "VERSION": config["bot"]["version"],
        "MEGASPAM_MAX": int(config["bot"]["megaspam_max"]),
        "PURGE_MAX": int(config["bot"]["purge_max"]),

        "YES_EMOJI": config["emoji"]["yes_emoji"],
        "NO_EMOJI": config["emoji"]["no_emoji"],

        "SNIPE_MESSAGE_PATH": SNIPE_MESSAGE_PATH,
        "LOGS_PATH": config["files"]["logs_path"],
        "SNIPE_PATH": config["files"]["snipe_path"],
        "IMAGES_PATH": config["files"]["images_path"],
        "VC_FILES_PATH": config["files"]["vc_files_path"],
        "VC_DOWNLOAD_PATH": config["files"]["vc_download_path"],
        "HELP_FILES_PATH": config["files"]["help_files_path"],
        "SYNTAX_FILES_PATH": config["files"]["syntax_files_path"],
        "FFMPEG_EXEC_PATH": config["files"]["ffmpeg_exec_path"],
        "BLACKLIST_PATH": BLACKLIST_PATH,

        "WEBHOOK_SERVER": config["webhook"]["webhook_server"],
        "USE_WEBHOOK": config["webhook"]["use_webhook"],

        "bl_server": file_read(BLACKLIST_PATH, "server.txt"),
        "bl_channel": file_read(BLACKLIST_PATH, "channel.txt"),
        "bl_response_server": file_read(BLACKLIST_PATH, "response_server.txt"),
        "bl_response_channel": file_read(BLACKLIST_PATH, "response_channel.txt"),
        "bl_role": file_read(BLACKLIST_PATH, "role.txt"),
        "bl_user": file_read(BLACKLIST_PATH, "user.txt"),

        "snipe_message": snipe_message_yml["snipe_message"]
    }

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

# appends text to a file of the given name
def file_append(file_path: str, file_name: str, text: str):
    with open(file_path + file_name, "a", encoding = "utf-8") as file:
        file.write(text)

# writes text to given file, deletes what was previously there
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

# Invalid command handler
async def invalid_command(config: dict, message, command: str):
    await send_r(message, message, f"[Error Handler]: \"**{command}**\" is not a valid command\n(try `hesa help`)")
    await message.add_reaction(config["NO_EMOJI"])

# runs when the main bot loop is closed
def exit_handler(config: dict):
    print(f"{col.Fore.YELLOW}>[Exit Handler]: Closing bot.")
    log(config["LOGS_PATH"], f"LOG-{get_date_time(1)}", f">[Exit Handler]: Closing bot.")
    print(f"{col.Style.RESET_ALL}Closed")

# used for the syntax command
def syntax_embed(config: dict, command):
    return discord.Embed(title = f"Syntax Help: {command}", description = file_read(config["SYNTAX_FILES_PATH"], f"{command}.txt"), color = config["EMBED_COLOR"])

# splits a string at the nth occurrence of a char
def split_nth(string: str, split_char: str, nth_occurrence: int):
    temp = string.split(split_char)
    return split_char.join(temp[:nth_occurrence]), split_char.join(temp[nth_occurrence:])

# Logs a message to the logs webhook
def webhook_log(config: dict, webhook_message: str):
    webhook = discord.SyncWebhook.from_url(config["WEBHOOK_URL"])
    webhook.send(content = webhook_message)

# Takes a string as input and replaces all of the var indicators with the provided values
def var_parser(input_string: str, var_names: list, replace_vars: list):
    for var, replace_var in zip(var_names, replace_vars):
        input_string = input_string.replace("{{" + var + "}}", replace_var)

    return input_string


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
