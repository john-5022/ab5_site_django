# z_jrp/wpac_jmp_reformat.py
# This reads the source file, transforms as per Xero then writes the dest file for Xero import
# Source file must be in same folder as this file and the name below
import csv

source_file = "C://ab5_Python/ab5_site_django/z_jrp/Wpac JMP.csv"
dest_file = "C://ab5_Python/ab5_site_django/z_jrp/Wpac JMP for Xero.csv"

dest_csv = []  # List for header and reformatted data

with open(source_file, mode="r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            csv_row = "Date", "Narrative", "Amount"
        else:
            debit = float(row["Debit Amount"]) if row["Debit Amount"] else 0
            credit = float(row["Credit Amount"]) if row["Credit Amount"] else 0
            amount = credit - debit
            csv_row = row["Date"], row["Narrative"], amount
        dest_csv.append(csv_row)
        line_count += 1

with open(dest_file, "w", encoding="UTF8", newline="") as f:
    writer = csv.writer(f)

    # write multiple rows - replace the file
    writer.writerows(dest_csv)
