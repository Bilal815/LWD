from django.urls import path
from . import views


urlpatterns = [
    path("api/create-device/", views.CreateDeviceAPIView.as_view()),
    path("api/notifications/", views.NotificationListView.as_view()),
    path("api/notifications/<int:pk>/", views.NotificationAPIView.as_view()),
    path("api/mark-all-as-read/", views.MarkedAllAsReadNotificationView.as_view()),
]
