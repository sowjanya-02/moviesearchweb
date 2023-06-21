from django.db import models

#from django.contrib.auth.models import User

class User(models.Model):
    #user = models.OneToOneField(, on_delete=models.CASCADE)
    # Add additional fields specific to your user profile
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    

