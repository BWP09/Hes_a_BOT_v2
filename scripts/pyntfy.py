import requests


def Priority(name: str | int):
    priority_id = 3
    
    match name:
        case "MIN": priority_id = 1
        case "LOW": priority_id = 2
        case "DEFAULT" | "NORMAL": priority_id = 3
        case "HIGH": priority_id = 4
        case "MAX": priority_id = 5
        
        case 1: priority_id = 1
        case 2: priority_id = 2
        case 3: priority_id = 3
        case 4: priority_id = 4
        case 5: priority_id = 5
    
    return {"p": str(priority_id)}

def Title(title: str):
    return {"t": title}

def Tags(*tags: str):
    if len(tags) == 1:
        return {"ta": str(tags[0])}

    final_tags = ""
    for tag in tags:
        final_tags += f"{tag},"
    
    final_tags = final_tags.removesuffix(",")
    
    return {"ta": final_tags}
        
def File(path: str, use_case: int = 0):
    if use_case == 0:
        return open(path, "rb")
    elif use_case == 1:
        return {"f": path.split("/")[-1]}

def Attach(link: str):
    return {"a": link}

def Icon(link: str):
    return {"Icon": link}

def Email(email: str):
    return {"e": email}


def ntfy(
        topic_url: str, content: str,
        headers: dict = {},
        title: dict = {},
        priority: dict = {},
        tags: dict = {},
        filename: dict = {},
        attachment: dict = {},
        icon: dict = {},
        email: dict = {}
        ):

    requests.post(
        topic_url,
        data = content,
        headers = {**headers, **title, **priority, **tags, **filename, **attachment, **icon, **email}
    )