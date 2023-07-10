# z_jrp/music_files_to_csv.py
# This is no longer needed - there a couple pf examples worth keeping
# Could not get eyed3 to work so uninstalled it

import os

# import eyed3
import csv

folder_names = []
mp3_details = []
wma_names = []

# rootdir = "G:\\Music Test"
rootdir = "D:\\Music on D\\For Python"

# Add all subfolders of rootvar (add the rootdir if needed) to folder_names list
for rootdir, dirs, files in os.walk(rootdir):
    for subdir in dirs:
        # print(os.path.join(rootdir, subdir))
        folder_names.append(os.path.join(rootdir, subdir))

# Scan the folder names list then handle music files when found
for folder_name in folder_names:
    # Load just the files in the current folder to file_list (listdir includes child folders)
    _, _, file_list = next(os.walk(folder_name))
    for file_name in file_list:  # os.scandir(folder_name):
        # Is it a music file?
        if file_name.rfind(".wma") > 0:
            # eyed3 only  works on .mp3 - not.wma files
            # path_file = os.path.join(folder_name, file_name)
            to_append = folder_name, file_name
            wma_names.append(to_append)

        if file_name.rfind(".mp3") > 0:
            # ToDo - get proerties then add to csv file

            # path_file = os.path.join(folder_name, file_name)
            # audio = eyed3.load(path_file)

            # album_artist = audio.tag.artist
            # album = audio.tag.album
            # title = audio.tag.title
            # genre = audio.tag.genre
            # length = audio.tag.length
            # # rating = audio.tag.rating

            # to_append = f"{folder_name}\{file_name}"
            to_append = (folder_name, file_name)
            mp3_details.append(to_append)

header = ["folder", "file"]

# Send any wma details to csv
with open("D:\\wma files.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.writer(f)

    # write the header
    header = ["folder", "file"]
    writer.writerow(header)

    # write multiple rows - there should be none
    writer.writerows(wma_names)

# Now the mp3s
with open("D:\\mp3 files.csv", "w", encoding="UTF8", newline="") as f:
    writer = csv.writer(f)

    # write the header
    # header = ["folder", "file", "title", "album_artist", "album", "genre", "length"]
    header = ["folder", "file"]
    writer.writerow(header)

    # write multiple rows
    writer.writerows(mp3_details)
