import pickle
import os
import lang
import kernel

users: list = []
folders: list = []
files: list = []
rootpass = lang.langkey("hover-pls")

os.makedirs("nebos", exist_ok=True)

def savesys(path:str = "nebos/save.pkl"):
    'save everything into a pickle'
    codedusers = [user.tojson() for user in users]
    tosave = {
        "users": codedusers,
        "folders": folders,
        "files": files,
        "root_password": rootpass
    }
    with open(path, "wb") as f:
        pickle.dump(tosave, f)
    print("Data saved!")

def loadsys(path:str = "nebos/save.pkl"):
    'load from the pickle'
    global users, folders, files
    try:
        with open(path, "rb") as f:
            data:dict = pickle.load(f)
        print(f"Loading {data}")

        codedusers = data.get("users", [])
        
        users.clear()
        users.extend([kernel.User.fromjson(usr) for usr in codedusers])
        
        folders.clear()
        folders.extend(data.get("folders", []))

        files.clear()
        files.extend(data.get("files", []))

        print("Data loaded!")
    except FileNotFoundError:
        print("No save file found, starting fresh.")
