from django.urls import path, include
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserChangePasswordView,
    SendPasswordResetEmailView,
    UserResetPasswordView,
    SendOtpView,
    VerifyOtpView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("me/", UserProfileView.as_view(), name="profile"),
    # path("update/", UserUpdateProfileView.as_view(), name="update_profile"),
    path("changepassword/", UserChangePasswordView.as_view(), name="changepassword"),
    path("send-otp/", SendOtpView.as_view(), name="sendotp"),
    path(
        "send-reset-password-email/",
        SendPasswordResetEmailView.as_view(),
        name="sendresetemail",
    ),
    path("verify-otp/", VerifyOtpView.as_view(), name="verifyotp"),
    path(
        "resetpassword/<uid>/<token>/",
        UserResetPasswordView.as_view(),
        name="resetpassword",
    ),
]
