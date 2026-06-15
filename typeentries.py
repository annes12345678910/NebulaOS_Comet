types = {
    "IMAGE": [
        "bmp",
        "png",
        "jpeg",
        "jpg",
        "tga",
        "gif",
        "qoi",
        "psd",
    ],
    "AUDIO": [
        "mp3",
        "wav",
        "ogg",
        "flac",
        "qoa",
        "xm",
        "mod"
    ],
    "TEXT": [
        "txt",
        "nsm",
        "py",
        "json",
        "csv"
    ]
}

entries = {
    "IMAGE":"./system/programs/viewer.nsm",
    "AUDIO":"./system/programs/player.nsm",
    "":"./system/programs/template.nsm",
    "TEXT":"./system/programs/edittext.nsm"
}

def getextgroup(ext):
    for key,value in types.items():
        for i in value:
            if ext == i:
                return key
    return ""
