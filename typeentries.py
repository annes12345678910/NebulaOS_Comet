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
    ]
}

entries = {
    "IMAGE":["./system/programs/viewer.nsm"],
    "AUDIO":["./system/programs/player.nsm"]
}

def getextgroup(ext):
    for key,value in types.items():
        for i in value:
            if ext == i:
                return key
    return ""
