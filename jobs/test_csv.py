# test_csv.py
import csv

file_name = "./jobs_etc.csv"

with open(file_name, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    ##########
    # Each row is a dictionary with the keys as per the header row
    ##########
    result = ""
    for row in reader:
        if row["Client_id"]:
            client_id = row["Client_id"]
            result = result + f"{client_id}"
        if row["Job"]:
            job = row["Job"]
            result = result + f"{job}"
        if row["Task"]:
            task = row["Task"]
        if row["Action"]:
            action = row["Action"]

    print(result)
