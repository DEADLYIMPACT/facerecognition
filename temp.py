import csv
with open("details.csv", 'r') as csvFile:
    print(csvFile)
    output = csv.reader(csvFile)
    for row in output:
        print(row)
        if len(row) > 0:
            if row[0] == Id and row[1] != name:
                print("Id aldready exists for a different user")
                return False     