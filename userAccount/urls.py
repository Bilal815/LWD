from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from rest_framework import routers
from rest_auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
    LogoutView,
)
from rest_auth.registration.views import RegisterView, VerifyEmailView

router = routers.DefaultRouter()
router.register('ids', views.NationalIDImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("login/", views.LoginAPIView.as_view(), name="account_login"),
    path(
        "reset/password/", views.PasswordResetView.as_view(), name="rest_password_reset"
    ),
    path(
        "password/change/",
        views.PasswordChangeView.as_view(),
        name="rest_password_change",
    ),
    path("api/", include("rest_auth.urls")),
    path("api/registration/", views.RegisterAPIView.as_view(), name="account_signup"),
    path("api/registration/", include("rest_auth.registration.urls")),
    path("api/logout/", LogoutView.as_view(), name="rest_logout"),
    path(
        "api/account-confirm-email/sent/",
        TemplateView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "api/account-confirm-email/<str:key>",
        views.VerifyEmailView.as_view(),
        name="rest_verify_email",
    ),
    path(
        "api/password/reset/confirm/<str:uidb64>/<str:token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("api/verify-sms/<int:pk>/", views.VerifySMSView.as_view()),
    path("api/resend-sms/", views.ResendSMSAPIView.as_view()),
    path("api/deactive-user/", views.DeactivateUserView.as_view()),
    path("api/reactive-user/", views.CanselDeactivateUserView.as_view()),
    path("api/profile/<int:pk>/", views.ProfileAPIView.as_view()),
    path("api/user/<str:username>/", views.UserDetailView.as_view()),
    path("api/addresses/", views.ListAddressAPIView.as_view()),
    path("api/address/<int:pk>", views.AddressDetailView.as_view()),
    path("api/create/address/", views.createAddressAPIView.as_view()),
    path("api/facebook/", views.FacebookConnectView.as_view()),
    path("api/twitter/", views.TwitterConnectView.as_view()),
    path("api/perm/<str:username>/", views.RetrievePermissionView.as_view()),
    path("api/perm/<str:username>/update/", views.UpdatePermissionView.as_view()),
]
