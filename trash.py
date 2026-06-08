"Trash compactor"

import os
import kernel,zipfile,pathlib

trashfiles:list[kernel.File] = []
trashfolders:list[kernel.Folder] = []

compactedata:bytes = b''

def compressall():
    global compactedata
    with zipfile.ZipFile("nbc_cache/trash.7z", "w", zipfile.ZIP_LZMA) as f:
        # use ligma
        for folder in trashfolders:
            f.mkdir(folder.name)

        for file in trashfiles:
            zipinfo = zipfile.ZipInfo(f"{file.getvisual(kernel.root)}")
            #zipinfo.date_time = file.date_created
            zipinfo.compress_type = zipfile.ZIP_LZMA
            f.writestr(zipinfo, file.contents)
    
    with open("nbc_cache/trash.7z", "rb") as f:
        compactedata = f.read()

    trashfiles.clear()
    trashfolders.clear()

def read_compact():
    global compactedata
    with open("nbc_cache/trash.7z", "wb") as f:
        f.write(compactedata)
    
    compactedata = b''

    with zipfile.ZipFile("nbc_cache/trash.7z", "r", zipfile.ZIP_LZMA) as f:
        os.makedirs("nbc_cache/trash", exist_ok=True)
        f.extractall("nbc_cache/trash")
        e = pathlib.Path("nbc_cache/trash")

def test():
    wow = kernel.Folder(kernel.root, "Wow")
    trashfiles.append(kernel.File(wow, "poo", "txt"))
    trashfolders.append(wow)
    compressall()

if __name__ == "__main__":
    test()
