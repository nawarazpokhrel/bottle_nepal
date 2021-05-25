from django.urls import path

from apps.users import views

urlpatterns = [
    path(
        'register',
        views.RegisterUserView.as_view(),
        name='register-new-user'
    ),
    path(
        'activate-by-email',
        views.VerifyEmailAndSubscribeEmailView.as_view(),
        name='activate-by-email'
    ),
]
