from rest_framework import serializers
from .models import UserAccount
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Util
import random


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["email", "name", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                "password and confirm password didn't matched"
            )
        return attrs

    def create(self, validated_data):
        return UserAccount.objects.create_user(
            **validated_data,
            # first_name=None,
            # last_name=None,
            # date_of_birth=None,
            # gender="O",
            # mobile=None,
            # aboutmovieLife=None
        )


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ["email", "password"]

    email = serializers.CharField(max_length=255)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = [
            "profile_picture",
            "email",
            "email_verified",
            "name",
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "mobile",
            "aboutmovieLife",
        ]


class UserUpdateProfileSerializer(serializers.Serializer):
    # first_name = serializers.CharField(max_length=255)
    # last_name = serializers.CharField(max_length=255)
    # gender = serializers.CharField(max_length=255)
    # date_of_birth = serializers.DateField()
    # aboutmovieLife = serializers.CharField()
    # mobile = serializers.IntegerField()

    class Meta:
        model = UserAccount
        fields = [
            "first_name",
            "last_name",
            "date_of_birth",
            "gender",
            "mobile",
            "aboutmovieLife",
        ]

    def update(self, instance, validated_data):
        # Update and return the instance with the validated data
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.date_of_birth = validated_data.get(
            "date_of_birth", instance.date_of_birth
        )
        instance.gender = validated_data.get("gender", instance.gender)
        instance.mobile = validated_data.get("mobile", instance.mobile)
        instance.aboutmovieLife = validated_data.get(
            "aboutmovieLife", instance.aboutmovieLife
        )
        instance.save()
        return instance

    # def validate(self, attrs):
    #     first_name = attrs.get("first_name")
    #     last_name = attrs.get("last_name")
    #     date_of_birth = attrs.get("date_of_birth")
    #     gender = attrs.get("gender")
    #     mobile = attrs.get("mobile")
    #     aboutmovieLife = attrs.get("aboutmovieLife")
    #     user = self.context.get("user")
    #     if user:
    #         user.first_name = first_name
    #         user.last_name = last_name
    #         user.date_of_birth = date_of_birth
    #         user.gender = gender
    #         user.mobile = mobile
    #         user.aboutmovieLife = aboutmovieLife
    #         user.save()
    #     return attrs


class UserChangePassSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user = self.context.get("user")
        if password != password2:
            raise serializers.ValidationError(
                "password and confirm password didn't matched"
            )
        user.set_password(password)
        user.save()
        return attrs


class SendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if UserAccount.objects.filter(email=email).exists():
            user = UserAccount.objects.get(email=email)
            otp = random.randint(100000, 999999)
            email_data = {
                "email_subject": "Verify Email for CineQuest Account",
                "email_body": "Hey "
                + user.name
                + ",\n"
                + "This is an auto generated Email from CineQuest-Img.Here is your  otp \n"
                + str(otp)
                + " \nOtp valid only for 10 minutes ",
                "email_to": email,
            }
            Util.sendEmail(email_data)
            user.verification_otp = otp
            user.save()

            return attrs
        else:
            raise serializers.ValidationError("Not a registered email ")


class OTPverifySerializer(serializers.Serializer):
    verification_otp = serializers.IntegerField()
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["verification_otp", "email"]

    def validate(self, attrs):
        verification_otp = attrs.get("verification_otp")
        email = attrs.get("email")
        if UserAccount.objects.filter(email=email).exists():
            user = UserAccount.objects.get(email=email)
            if verification_otp == user.verification_otp:
                user.email_verified = True
                user.verification_otp = 0
                user.save()

                return attrs

        return serializers.ValidationError("OTP didn't matched")


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if UserAccount.objects.filter(email=email).exists():
            user = UserAccount.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = "http://localhost:3000/auth/reset/" + uid + "/" + token
            print(link)
            email_data = {
                "email_subject": "Password Reset Auto Generated Mail",
                "email_body": "Hey "
                + user.name
                + ",\n"
                + "This is an auto generated Email from CineQuest-Img.Click the link below to reset password \n"
                + link
                + " \nLink valid only for 20 minutes ",
                "email_to": email,
            }
            Util.sendEmail(email_data)

            return attrs
        else:
            raise serializers.ValidationError("Not a registered email ")


class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            password2 = attrs.get("password2")
            uid = self.context.get("uid")
            token = self.context.get("token")
            if password != password2:
                raise serializers.ValidationError(
                    "password and confirm password didn't matched"
                )
            id = smart_str(urlsafe_base64_decode(uid))
            user = UserAccount.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    "Token is expired or not valid try again"
                )
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is expired or not valid try again")
