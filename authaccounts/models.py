from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _

from datetime import datetime


def upload_to(instance, filename):
    return "profile_images/{filename}".format(filename=filename)


# Create your models here.


class UserAccountManager(BaseUserManager):
    def create_user(
        self,
        email,
        name,
        # first_name,
        # last_name,
        # date_of_birth,
        # mobile,
        # aboutmovieLife,
        # gender,
        password=None,
        password2=None,
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            # first_name=first_name,
            # last_name=last_name,
            # date_of_birth=date_of_birth,
            # mobile=mobile,
            # aboutmovieLife=aboutmovieLife,
            # gender=gender,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    MALE = "M"
    FEMALE = "F"
    OTHERS = "O"
    GENDER_CHOICES = [(MALE, "Male"), (FEMALE, "Female"), (OTHERS, "others")]
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    profile_picture = models.ImageField(
        _("Image"), upload_to=upload_to, default="profile_images/defaultprofile.png"
    )
    email_verified = models.BooleanField(default=False)
    verification_otp = models.PositiveBigIntegerField(default=0)
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    gender = models.CharField(
        max_length=255, choices=GENDER_CHOICES, default=OTHERS, null=True
    )
    date_of_birth = models.DateField(auto_now_add=True)
    aboutmovieLife = models.TextField(null=True)
    mobile = models.BigIntegerField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
