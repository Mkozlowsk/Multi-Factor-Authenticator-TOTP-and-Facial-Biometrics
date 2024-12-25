import pyotp
import qrcode
import cv2
import face_recognition
import base64
import numpy as np
from io import BytesIO
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm, OTPForm
from .models import CustomUser

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.totp_secret = pyotp.random_base32()
            user.save()
            # return redirect('show_qr_code', user_id=user.id)
            return redirect('register_face', user_id=user.id)
    else:
        form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})


def register_face(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == 'POST':
        # Pobranie kodowania twarzy z kamery
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return render(request, 'authentication/register_face.html', {'error': 'Can\'t connect to camera'})

        face_locations = face_recognition.face_locations(frame)
        if len(face_locations) != 1:
            return render(request, 'authentication/register_face.html',
                          {'error': 'Make sure one face is visible'})

        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
        user.set_face_encoding(face_encoding)
        user.save()
        return redirect('show_qr_code', user_id=user.id)

    return render(request, 'authentication/register_face.html')


def show_qr_code(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    totp = pyotp.TOTP(user.totp_secret)
    url = totp.provisioning_uri(user.username, issuer_name="BemsiProject")

    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    image_base64 = base64.b64encode(image_stream).decode('utf-8')

    return render(request, 'authentication/show_qr_code.html', {'qr_code': image_base64})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pre_2fa_user_id'] = user.id
            return redirect('verify_otp')
    return render(request, 'authentication/login.html')

def verify_otp(request):
    if request.method == "POST":
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            user_id = request.session.get('pre_2fa_user_id')
            user = CustomUser.objects.get(id=user_id)
            totp = pyotp.TOTP(user.totp_secret)
            if totp.verify(otp):
                login(request, user)
                # return redirect('register')
                return redirect('login_with_face')
    else:
        form = OTPForm()
    return render(request, 'authentication/verify_otp.html', {'form': form})


def login_with_face(request):
    if request.method == 'POST':
        # Pobranie kodowania twarzy z kamery
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return render(request, 'authentication/login_with_face.html', {'error': 'Can\'t connect to camera'})

        face_locations = face_recognition.face_locations(frame)
        if len(face_locations) != 1:
            return render(request, 'authentication/login_with_face.html', {'error': 'Make sure one face is visible'})

        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

        # Porównanie kodowania twarzy z kodowaniem w bazie danych
        users = CustomUser.objects.exclude(face_encoding__isnull=True)
        for user in users:
            if face_recognition.compare_faces([user.get_face_encoding()], face_encoding)[0]:
                login(request, user)
                return redirect('register')
                # return redirect('home')

        return render(request, 'authentication/login_with_face.html', {'error': 'Nie znaleziono dopasowania.'})

    return render(request, 'authentication/login_with_face.html')


