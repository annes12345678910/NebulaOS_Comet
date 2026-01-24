import pickle
import os
import lang

users: list = []
folders = []
files = []
rootpass = lang.langkey("hover-pls")

os.makedirs("nebos", exist_ok=True)

def savesys():
    tosave = {
        "users": users,
        "folders": folders,
        "files": files,
        "root_password": rootpass
    }
    with open("nebos/save.pkl", "wb") as f:
        pickle.dump(tosave, f)
    print("Data saved!")

def loadsys():
    global users, folders, files
    try:
        with open("nebos/save.pkl", "rb") as f:
            data:dict = pickle.load(f)
        users = data.get("users", [])
        folders = data.get("folders", [])
        files = data.get("files", [])
        print("Data loaded!")
    except FileNotFoundError:
        print("No save file found, starting fresh.")
