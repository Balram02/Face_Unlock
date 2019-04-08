from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Users
import cv2
from django.http.response import StreamingHttpResponse
from .facerecognize import face_identify
from django.urls import reverse
from F_R.settings import STATIC_DIR
import os
import shutil
from threading import Timer
import threading
import time
import numpy as np

message = {'msg': '', 'for_detail': True, 'for_image': False, }
camera_port = 0


class variables:
    faceCounter = 0
    users = Users()
    actual_image = ''
    reached_10 = False
    registration = False
    login = False
    directory_name = ''
    stored = False
    camera = cv2.VideoCapture()
    identified = False


cl = variables()


def on_complete():
    message['msg'] = 'Please login again'
    message['for_detail'] = True
    message['for_image'] = False


t = Timer(0.5, on_complete)


def create_dir():
    try:
        path = STATIC_DIR + '/database/' + cl.directory_name
        if os.makedirs(path, 0o755):
            shutil.rmtree(path + cl.directory_name, ignore_errors=True)
    except OSError as e:
        print("error = " + str(e))


def get_frames():
    face_cascade = cv2.CascadeClassifier(STATIC_DIR + "/haarcascade/haar_front_face_default.xml")
    eye_cascade = cv2.CascadeClassifier(STATIC_DIR + "/haarcascade/haarcascade_eye.xml")
    if cl.camera.isOpened():
        cl.camera.release()
        cl.camera = cv2.VideoCapture(camera_port)

    while True:
        if not cl.camera.isOpened():
            cl.camera = cv2.VideoCapture(camera_port)
        retval, frame = cl.camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.flip(frame, 180)
        cl.actual_image = frame
        if cl.registration and not cl.reached_10:
            save_data_frames(frame)
        elif cl.registration and cl.reached_10 and not cl.stored:
            cl.users.save()
            cl.stored = True
            message['for_detail'] = True
            message['for_image'] = False
        if cl.login:
            print("i m in")
            print(np.array(frame))
            cl.identified = face_identify(frame, cl.directory_name)

        face = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)

        print('Faces found in the image', len(face))
        for (x, y, w, h) in face:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        img_encode = cv2.imencode('.jpg', frame)[1]
        string_data = img_encode.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: text/plain\r\n\r\n' + string_data + b'\r\n')


def save_data_frames(frame):
    (width, height) = (130, 100)
    for i in range(0, 10):
        frame_resize = cv2.resize(frame, (width, height))
        cv2.imwrite(STATIC_DIR + '/database/' + cl.directory_name + '/%d.jpg' % i, frame_resize)
        print("Saved frame number : ", i)
        print('at' + STATIC_DIR + '/database/' + cl.directory_name + '/%d.jpg' % i)
    cl.reached_10 = True


def frames(request):
    return StreamingHttpResponse(get_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


def home(request):
    if not request.session.get('user_logged_in'):
        return HttpResponseRedirect('register')
    return render(request, 'home.html')


def login(request):
    # if request.session.get('user_logged_in'):
    #     return HttpResponseRedirect('http://localhost:8000/')
    if cl.camera.isOpened():
        cl.camera.release()
    if message['for_image'] and not cl.registration:
        cl.login = True
    if message['msg'] and message['for_image']:
        # request.session['user_logged_in'] = True
        # request.session.set_expiry(300)
        cl.login = True
        return render(request, 'login.html', message)

    elif message['msg'] and not request.session.get('user_logged_in'):
        return render(request, 'login.html', message)
    # elif request.session.get('user_logged_in'):
    #     return render(request, 'home.html')
    else:
        request.session['user_logged_in'] = False
        return render(request, 'login.html', message)


def register(request):
    # if request.session.get('user_logged_in'):
    #     return HttpResponseRedirect('http://localhost:8000/')
    # else:
    #     request.session['user_logged_in'] = False
    return render(request, 'register.html', message)


@csrf_exempt
def register_user(request):
    if request.POST:
        if 'fullname' and 'email' and 'password' in request.POST:

            cl.users.email = request.POST['email']
            cl.users.password = request.POST['password']

            if ' ' in request.POST['fullname']:
                cl.users.first_name = request.POST['fullname'].split(' ')[0]
                cl.users.last_name = request.POST['fullname'].split(' ')[1]
            else:
                cl.users.first_name = request.POST['fullname']
                cl.users.last_name = ''
            if message['for_detail']:
                message['for_detail'] = False
                message['for_image'] = True
                cl.directory_name = cl.users.email.split('@')[0]
                create_dir()
                cl.registration = True
                t.start()
                return HttpResponseRedirect('http://localhost:8000/register/')
            else:
                cl.users.save()
                message['msg'] = "Please login again"
                message['for_detail'] = True
                message['for_image'] = False
                return HttpResponseRedirect('http://localhost:8000/login/')

    else:
        message['msg'] = 'There some error, Please try again'
        return render(request, 'register.html', message)


@csrf_exempt
def login_user(request):
    # if request.session.get('user_logged_in'):
    #     return HttpResponseRedirect('http://localhost/')
    if request.POST:
        if 'email' and 'password' in request.POST:
            email = request.POST['email']
            password = request.POST['password']
            is_user = Users.objects.filter(email=email, password=password)
            if is_user:
                cl.directory_name = email.split('@')[0]
                message['for_image'] = True
                message['for_detail'] = False
                return HttpResponseRedirect('http://localhost:8000/login/')
            else:
                message['msg'] = 'Email or Password is incorrect'
                return render(request, 'login.html', message)
        else:
            message['msg'] = 'There was error !'
            return render(request, 'login.html', message)
    else:
        return HttpResponseRedirect('http://localhost:8000/not_found/')


def identify(request):
    if cl.camera.isOpened():
        cl.camera.release()
    if cl.identified:
        request.session['user_logged_in'] = True
        if cl.camera.isOpened():
            cl.camera.release()
        return HttpResponseRedirect('http://localhost/')
    message['msg'] = "Face not found, Try again"
    message['for_image'] = False
    message['for_detail'] = True
    return redirect('http://localhost:8000/login/')


def not_found(request):
    return render(request, 'not_found.html')
