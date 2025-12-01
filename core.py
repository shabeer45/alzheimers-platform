from database import *
from flask import *
import demjson
import numpy as np
from model_manager import Model
import pickle
import math
import cv2
import uuid
import face_recognition
import argparse
from imutils import paths
import os
import requests
import io
import json
from database import *
from datetime import datetime

def get_max_login_id():
	q = "select max(login_id) as  max from login"
	res = select(q)
	print(res[0]['max'])
	if res:
		return res[0]['max']
	else:
		return 0

def create_matrix():
	max_id = get_max_login_id()
	matrix = []
	for i in range(0,max_id+1):
		row = []
		for j in range(0,max_id+1):
			m = Model(i,j)
			row.append(m)
		matrix.append(row)
	for i in range(0,max_id+1):
		for j in range(0,max_id+1):
			matrix[j][i] = matrix[i][j]
	return matrix

def pre_process_features(features):
	temp = []
	for f in features:
		if len(f) == 6 and None not in f:
			temp.append(f)
	if temp:
		temp = temp / np.max(temp)
		temp = np.asarray(temp)
	return np.asarray(features)

def train_matrix(matrix,user1,user2):
	user_1_id = user1['login_id']
	user_2_id = user2['login_id']
	# print((user1['features']))
	# print((user2['features']))

	user_1_features = pre_process_features(demjson.decode(user1['features']))
	user_2_features = pre_process_features(demjson.decode(user2['features']))

	user_1_op = np.asarray([user_1_id] * user_1_features.shape[0])
	user_2_op = np.asarray([user_2_id] * user_2_features.shape[0])
	
	# X_train = np.append(user_1_features,user_2_features,axis=0)
	# Y_train = np.concatenate((user_1_op,user_2_op),axis=0)
	matrix[user_1_id][user_2_id].train(user_1_features,user_2_features,user_1_op,user_2_op)
	matrix[user_2_id][user_1_id].train(user_1_features,user_2_features,user_1_op,user_2_op)

def train():
	matrix = create_matrix()
	q = "select * from login"
	res = select(q)
	for i in range((len(res))):
		for j in range((len(res))):
			user1 = res[i]
			user2 = res[j]
			train_matrix(matrix,user1,user2)
	file = open("model.pickle","wb")
	pickle.dump(matrix,file)
	file.close()

def predict(matrix,id1,id2,features):
	if id1 > -1 and id2 > -1:
		res = matrix[id2][id1].predict(features)
		print(matrix[id2][id1])
	elif id1 > -1:
		res = id1
	elif id2 > -1:
		res = id2
	else:
		res = -1
	return res

def predict_from_array(matrix,array,features):
	print(array)
	new_layer = []
	if len(array) > 1:
		for i in range((len(array) - 1)):
			user1 = array[i]
			user2 = array[i+1]
			new_layer.append(predict(matrix,user1,user2,features))
		if len(new_layer) == 1:
			return new_layer[0]
	else:
		user1 = array[0]
		user2 = array[0]
		return predict(matrix,user1,user2,features)
	return predict_from_array(matrix,new_layer,features)

def get_login_id(features):
	file = open("model.pickle","rb")
	matrix = pickle.load(file)
	file.close()
	features = pre_process_features(demjson.decode(features))
	q = "select * from login"
	res = select(q)
	layer = []
	for row in res:
		layer.append(row['login_id'])
	id = predict_from_array(matrix,layer,features)
	return id

# camera for image testing
def val(ids,path):
	size = 4
	print("------------",path)

	# We load the xml file
	classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	
	# webcam = cv2.VideoCapture(path) #Using default WebCam connected to the PC.
	# # (rval, im) = webcam.read()
	# # flag=0
	# # while True:
	# (rval, im) = webcam.read()
	im = cv2.imread(path)
	img_cw_180 = cv2.rotate(im, cv2.ROTATE_90_CLOCKWISE)
	# im = cv2.rotate(im, cv2.ROTATE_90_COUNTERCLOCKWISE)
	FaceFileName = "static/test.jpg" #Saving the current image from the webcam for testing.
		

	cv2.imwrite(FaceFileName, img_cw_180)
	im=cv2.flip(img_cw_180,1,0) #Flip to act as a mirror

	# Resize the image to speed up detection
	mini = cv2.resize(im, (int(im.shape[1]/size), int(im.shape[0]/size)))

	# detect MultiScale / faces 
	faces = classifier.detectMultiScale(mini)

	# Draw rectangles around each face
	flag=0
	val=0
	for f in faces:
		print("==============================")
		(x, y, w, h) = [v * size for v in f] #Scale the shapesize backup
		cv2.rectangle(im, (x,y), (x+w,y+h), (0,255,0), 4)
		#Save just the rectangle faces in SubRecFaces
		sub_face = im[y:y+h, x:x+w]
		FaceFileName = "static/test.jpg" #Saving the current image from the webcam for testing.
		cv2.imwrite(FaceFileName, sub_face)
		val=rec_face_image(FaceFileName)
		print("pppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp")
		print(val)
		str1=""
		for ele in val:  
			str1 = ele
		print(str1)
		val=str1.replace("'","")
		
	return val
	
	

def rec_face_image(imagepath):
    print(imagepath)
    data = pickle.loads(open('faces.pickles', "rb").read())

    # load the input image and convert it from BGR to RGB
    image = cv2.imread(imagepath)
    #print(image)
    h,w,ch=image.shape
    print(ch)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # detect the (x, y)-coordinates of the bounding boxes corresponding
    # to each face in the input image, then compute the facial embeddings
    # for each face
    print("[INFO] recognizing faces...")
    boxes = face_recognition.face_locations(rgb,model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes)

    # initialize the list of names for each face detected
    names = []

    # loop over the facial embeddings
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],encoding,tolerance=0.4)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            print(counts, " rount ")
	    
            # determine the recognized face with the largest number of
            # votes (note: in the event of an unlikely tie Python will
            # select first entry in the dictionary)
            if len(counts) == 1:
                name = max(counts, key=counts.get)
            else:
                name = "-1"
        # update the list of names
        # if name not in names:
        if name != "Unknown":
            names.append(name)
    return names

# image write or uploads
def enf(path):
        imagePaths = path
	
		# initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []
        for  fname in os.listdir(imagePaths):
            facedir=os.path.join(imagePaths,fname)
            for  imagePt in os.listdir(facedir):
                img=os.path.join(facedir,imagePt)
				# extract the person name from the image path
                print("[INFO] processing image {}/{}".format(fname,len(imagePt)))
                print("imagepath-------",imagePaths)
                # print(magePath.split(os.path.sep))
               
                name = fname
		
                # load the input image and convert it from RGB (OpenCV ordering)
                # to dlib ordering (RGB)
                image = cv2.imread(img)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # detect the (x, y)-coordnates of the bounding boxes
                # corresponding to each face in the input image
                boxes = face_recognition.face_locations(rgb,model='hog')

				# compute the facial embedding for the face
                encodings = face_recognition.face_encodings(rgb, boxes)

                # loop over the encodings
                for encoding in encodings:
                        # add each encoding + name to our set of known names and
                        # encodings
                        knownEncodings.append(encoding)
                        knownNames.append(name)
        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open('faces.pickles', "wb")
        f.write(pickle.dumps(data))
        f.close()

# OCR 
def ocrgenerate(image):
	print(image)
	img = cv2.imread(image)
	height, width, _ = img.shape
	# Cutting image
	# roi = img[0: height, 400: width]
	roi = img
	url_api = "https://api.ocr.space/parse/image"
	_, compressedimage = cv2.imencode(".jpg", roi, [1, 90])
	file_bytes = io.BytesIO(compressedimage)
	result = requests.post(url_api,
	              files = {"screenshot.jpg": file_bytes},
	              data = {"apikey": "f2c63a5eb288957",
	                      "language": "eng"})
	result = result.content.decode()
	result = json.loads(result)
	print(result)
	parsed_results = result.get("ParsedResults")[0]
	text_detected = parsed_results.get("ParsedText")
	return text_detected



# enf(r"static/trainimages/") 