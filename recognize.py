import os
import cv2
import time
import csv
def Recognize(frame):
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    recognizer.read("train.yml")
    detector = cv2.CascadeClassifier("face.xml")
    original = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(frame, 1.2, 5)
    for (x, y, w, h) in faces:
        Id, confidence = recognizer.predict(frame[y: y + h, x: x + w])
        cv2.rectangle(original, (x, y), (x + w, y + h), (0, 0, 255), 2)
        name = ""
        if confidence < 50:
            with open("details.csv", 'r') as csvFile:
                output = csv.reader(csvFile)
                for row in output:
                    if len(row) > 0:
                        if row[0] == str(Id):
                            name = row[1]               
            cv2.putText(original, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    return(original, name)                             

