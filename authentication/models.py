from django.contrib.auth.models import AbstractUser
from django.db import models
import numpy as np

# Create your models here.

class CustomUser(AbstractUser):
    totp_secret = models.CharField(max_length=16, blank=True, null=True)
    face_encoding = models.BinaryField(blank=True, null=True)

    def set_face_encoding(self, encoding):
        self.face_encoding = np.array(encoding).tobytes()
        self.save()

    def get_face_encoding(self):
        if self.face_encoding:
            return np.frombuffer(self.face_encoding, dtype=np.float64)
        return None