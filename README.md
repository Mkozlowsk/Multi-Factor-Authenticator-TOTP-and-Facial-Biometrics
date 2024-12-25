# Multi-Factor-Authenticator-TOTP-and-Facial-Biometrics

## Project Description
Project was transfered from internal academy server. This project was concluded in May 2024.
The project implements a multi-step authentication system in a web application to enhance the security of user account access. To increase the system’s security, TOTP codes and facial biometrics were used.

### Features
- TOTP keys
- Recognition of facial biometry

### Technologies and Tools
- **Python**  
- **Django**  
- **pyopt**  
- **qrcode**
- **openCV**
- **faceRecognition** 

### Installation
1. Clone the repository
2. Run the server with commands:
   ```b
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
3. To register enter the adress:
   ```b
    http://127.0.0.1:8000/register/
4. To login enter the adress:
   ```b
    http://127.0.0.1:8000/login/
