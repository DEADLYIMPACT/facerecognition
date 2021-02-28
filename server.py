from flask import Flask
from flask import render_template
from flask import Response
from flask import redirect
from flask import request
import cv2

import csv
import os
import sys
import threading
from recognize import Recognize

app = Flask(__name__)
lock = threading.Lock()
outputFrame = None
running = True

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

@app.route("/camera")
def camera():
	return render_template("camera.html")

@app.route("/")
def default():
	global running
	running = False
	return render_template("index.html")


@app.route("/capturePage", methods = ["POST"])
def callCapture():
	return render_template("capture.html")


@app.route("/capture", methods = ["POST"])
def capture():
	Name = request.form["Name"]
	Id = request.form["Id"]
	captureStream(32, Name, Id)
	return redirect("http://192.168.1.68:5000")


@app.route("/train", methods = ["POST"])
def train():
	import train
	train.run()
	return redirect("http://192.168.1.68:5000")


@app.route("/recognize", methods = ["POST"])
def recognize():
	global running
	running = True
	t = threading.Thread(target=detect_motion, args=(32,))
	t.daemon = True
	t.start()
	return render_template("recognize.html", d = "ABCD")


def detect_motion(frameCount):
	global vs, outputFrame, lock, running
	cap = cv2.VideoCapture(0)
	while running:
		ret, frame = cap.read()
		frame, name = Recognize(frame)
		with lock:
			outputFrame = frame.copy()
	cap.release()

	
def captureStream(frameCount, name, Id):
	global outputFrame, lock
	with open("details.csv", 'r') as csvFile:
		output = csv.reader(csvFile)
		for row in output:
			if len(row) > 0:
				if row[0] == Id and row[1] != name:
					print("Id aldready exists for a different user")
					return False
	if is_number(Id) and name.isalpha():
		vid = cv2.VideoCapture(0)
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
				#	 break   
				with lock:
					outputFrame = gray.copy()
			else:
				break

		res = "Images Saved for ID : " + Id + " Name : " + name
		row = [Id, name]

		with open("details.csv", 'a+') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(row)
		csvFile.close()

		return redirect("http://192.168.1.68:5000")


def generate():	
	global outputFrame, lock
	while True:
		with lock:
			if outputFrame is None:
				continue
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			if not flag:
				continue
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
	
	app.run(host="192.168.1.68", port=5000, debug=True,
		threaded=True, use_reloader=False)