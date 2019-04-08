#!/usr/bin/python

import face_recognition
import cv2
import os
from F_R.settings import STATIC_DIR
import numpy as np


def face_identify(actual_image, directory):
    path = STATIC_DIR + '/database/'
    # process_this_frame = True

    # image = []
    # encoded = []

    images = os.listdir(str(path + directory))

    # print(actual_image)

    encoded_image_to_be_matched = face_recognition.face_encodings(actual_image)
    print(encoded_image_to_be_matched)
    print("yahan pr")
    print(np.array(actual_image))
    # cv2.imread(actual_image)
    # cv2.imshow("hnks", actual_image)

    # for i in range(0, 10):
    #     # Change directory according to your system
    #     image = (face_recognition.load_image_file(path + "/" + name + "/" + str(i) + ".jpg"))
    #     encoded.insert(i, face_recognition.face_encodings(image))

    # image0 = (face_recognition.load_image_file(path + directory + "/0" + ".jpg"))
    # print(str(image0))
    # encoded0 = (face_recognition.face_encodings(image0)[0])
    # # print(str(image0))
    #
    # image1 = (face_recognition.load_image_file(path + directory + "/1" + ".jpg"))
    # encoded1 = (face_recognition.face_encodings(image1)[0])
    #
    # image2 = (face_recognition.load_image_file(path + directory + "/2" + ".jpg"))
    # encoded2 = (face_recognition.face_encodings(image2)[0])
    #
    # image3 = (face_recognition.load_image_file(path + directory + "/3" + ".jpg"))
    # encoded3 = (face_recognition.face_encodings(image3)[0])
    #
    # image4 = (face_recognition.load_image_file(path + directory + "/4" + ".jpg"))
    # encoded4 = (face_recognition.face_encodings(image4)[0])
    #
    # image5 = (face_recognition.load_image_file(path + directory + "/5" + ".jpg"))
    # encoded5 = (face_recognition.face_encodings(image5)[0])
    #
    # image6 = (face_recognition.load_image_file(path + directory + "/6" + ".jpg"))
    # encoded6 = (face_recognition.face_encodings(image6)[0])
    #
    # image7 = (face_recognition.load_image_file(path + directory + "/7" + ".jpg"))
    # encoded7 = (face_recognition.face_encodings(image7)[0])
    #
    # image8 = (face_recognition.load_image_file(path + directory + "/8" + ".jpg"))
    # encoded8 = (face_recognition.face_encodings(image8)[0])
    #
    # image9 = (face_recognition.load_image_file(path + directory + "/9" + ".jpg"))
    # encoded9 = (face_recognition.face_encodings(image9)[0])

    count = 0
    for image in images:
        if count != 10 and count <= 9:
            # current_image = (face_recognition.load_image_file(path + directory + "/" + str(count) + ".jpg"))
            current_image = cv2.imread(path + directory + "/" + str(count) + ".jpg")
            count += 1
            print(current_image)
            print(str(len(current_image)))
            if len(current_image) > 0:
                current_image_encoded = (face_recognition.face_encodings(current_image))
                print(str(len(current_image_encoded)))
                if len(current_image_encoded) > 0:
                    current_image_encoded = (face_recognition.face_encodings(current_image)[0])
                    known_encodings = [current_image_encoded]
                    # known_encodings = [0, actual_image.shape[1], actual_image.shape[0], 0]
                    small_frame = cv2.resize(np.array(actual_image), (0, 0), fx=0.25, fy=0.25)
                    rgb_small_frame = small_frame[:, :, ::-1]
                    face_locations = (face_recognition.face_locations(rgb_small_frame))
                    face_encodings = (face_recognition.face_encodings(rgb_small_frame, face_locations))

                    for face_encoding in face_encodings:
                        matched = face_recognition.compare_faces(known_encodings, face_encoding)

                        if True in matched:
                            print("got it")
                            print("under " + path + directory + "/5" + ".jpg")
                            # multiprocessing.Process(target=say_name, args=(directory,)).start()
                            return True
                        else:
                            print("galat hai")
                            print("under " + path + directory + "/5" + ".jpg")
                            # return False
        else:
            return False

# def face_recon():
# camera_port = 0
#    camera = cv2.VideoCapture(camera_port)
#    __, im = camera.read()
#    (width, height) = (130, 100)
#    haar_file = 'haar_front_face_default.xml'
#    face_cascade = cv2.CascadeClassifier(haar_file)
#    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
#    for (x,y,w,h) in faces:
#        cv2.rectangle(faces,(x,y),(x+w,y+h),(255,0,0),2)
#        face = gray[y:y + h, x:x + w]
#       face_resize = cv2.resize(face, (width, height))
