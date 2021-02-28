import Face_capture
import train
import recognize

while True:
    i = input("1  - Capture Face, 2 - Train model, 3 - Recognize Face ")
    if i == "1":
        Face_capture.run()
    elif i == "2":
        train.run()
    elif i == "3":
        recognize.Recognize(1)
    else:
        break           