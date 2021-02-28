import cv2

import numpy as np
import os
from PIL import Image

def getImageAndLabels(path):
    imagePath = [os.path.join(path, f) for f in os.listdir(path)]
    # print(imagePath)
    faces = []
    Ids = []
    for i in imagePath:
        image = Image.open(i).convert("L")
        imageNp = np.array(image, 'uint8')
        Id = int(os.path.split(i)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids    
def run():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    path = "face.xml"
    detector = cv2.CascadeClassifier(path)
    face, Id = getImageAndLabels(r"C:\Users\ASUS\Aakash\Coding\Python K12\Face detection\Images")
    recognizer.train(face, np.array(Id))
    recognizer.save("train.yml")