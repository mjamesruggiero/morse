import hashlib
import os
import shutil
from pathlib import Path

BLOCKSIZE = 65536

def hash_file(path):
    hasher = hashlib.sha1()
    with path.open("rb") as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)

    return hasher.hexdigest

def read_paths_and_hashes(root):
    hashes = {}
    for folder, _, files in os.walk(root):
        for fn in files:
            hashes[hash_file(Path(folder) / fn)] = fn
    return hashes


# def determine_actions(source_hashes, dest_hashes, source_folder, dest_folder):
#     for sha, filename in source_hashes.items():
#         if sha not in dest_hashes:
#             sourcepath = Path(source_folder) / filename
#             destpath = Path(dest_folder) / filename
#             yield "COPY", sourcepath, destpath
#         elif dest_hashes[sha] != filename:
#             olddestpath = Path(dest_folder) / dest_hashes[sha]
#             newdestpath = Path(dest_folder) / filename
#             yield "MOVE", olddestpath, newdestpath

#     for sha, filename in dest_hashes.items():
#         if sha not in source_hashes:
#             yield "DELETE", Path(dest_folder) / filename

class FileSystem:
    def read(self, path):
        return read_paths_and_hashes(path)

    def copy(self, source, dest):
        shutil.copyfile(source, dest)

    def move(self, source, dest):
        shutil.move(source, dest)

    def delete(self, dest):
        os.remove(dest)

def sync(source, dest, filesystem=FileSystem()):
    # imperative shell step 1: gather inputs
    source_hashes = filesystem.read(source)
    dest_hashes = filesystem.read(dest)

    for sha, filename in source_hashes.items():
        if sha not in dest_hashes:
            sourcepath = Path(source) / filename
            destpath = Path(dest) / filename
            filesystem.copy(sourcepath, destpath)
        elif dest_hashes[sha] != filename:
            olddestpath = Path(dest) / dest_hashes[sha]
            newdestpath = Path(dest) / filename
            filesystem.move(olddestpath, newdestpath)

    for sha, filename in dest_hashes.items():
        if sha not in source_hashes:
            filesystem.delete(dest / filename)
