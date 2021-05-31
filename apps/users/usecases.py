from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.email import ConfirmationEmail
from bottle_nepal.tasks import send_email

User = get_user_model()


class RegisterUserUseCase:
    """
    endpoint to register users
    """

    def __init__(self, serializer, request):
        self.serializer = serializer
        self._data = serializer.validated_data
        self._request = request

    def execute(self):
        self._factory()
        self._send_email()

    def _factory(self):
        password = self._data.pop('password')
        self._user = User(**self._data)
        self._user.set_password(password)
        self._user.save()
        try:
            # Get user
            self.user_instance = User.objects.get(
                id=self._user.id,
                email=self._data['email'],
                is_active=True
            )
        except User.DoesNotExist:
            raise ValidationError('User does not exists')

    def _send_email(self):
        token = RefreshToken.for_user(user=self.user_instance).access_token
        # get current site
        current_site = get_current_site(self._request).domain
        # we are calling verify by email view  here whose name path is activate-by-email
        relative_link = reverse('activate-by-email')
        # make whole url
        absolute_url = 'http://' + current_site + relative_link + "?token=" + str(token)
        self.context = {
            'user': self._user.username,
            'token': absolute_url
        }
        receipent = self._user.email
        send_email.delay(receipent, **self.context)

