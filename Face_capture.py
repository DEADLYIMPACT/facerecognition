import cv2
import csv
import os
import sys
def is_number(Id):
    try:
        float(Id)
        return True
    except ValueError:
        pass
    try: 
        import unicodedata
        unicodedata.numeric(Id)
        return True
    except(TypeError, ValueError):
        pass
    return False

def run(frame):
    # Id = input("ID:")
    # name = input("Your name: ")

    with open("details.csv", 'r') as csvFile:
        output = csv.reader(csvFile)
        for row in output:
            if len(row) > 0:
                if row[0] == Id and row[1] != name:
                    print("Id aldready exists for a different user")
                    return False   
    if is_number(Id) and name.isalpha():
        # vid = cv2.VideoCapture(0)
        faceCascade = cv2.CascadeClassifier("face.xml")
        count = 0
        while count < 200:
            ret, frame = vid.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if ret:
                face = faceCascade.detectMultiScale(gray, 1.1, 4)
                for(x, y, w, h) in face:
                    cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 0), 4)
                    count += 1
                    cv2.imwrite("Images" + os.sep + name + "." + Id + "." + str(count) + ".jpg", gray[y:y+h, x:x+w])
                # cv2.imshow("Frame", gray)
                # if cv2.waitKey(25) & 0xFF == ord('q'):
                #     break      
            else:
                break
        res = "Images Saved for ID : " + Id + " Name : " + name
        row = [Id, name]

        with open("details.csv", 'a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        return(gray)
    else:
        if not is_number(Id):
            print("Invalid Id")
        if not name.isalpha():
            print("Invalid Name")   