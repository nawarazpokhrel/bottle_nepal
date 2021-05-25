from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            'username',
            'email',
            'password',
        )

        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    default_error_messages = {
        'duplicate_email': _('Email  already exists.')
    }

    def validate_email(self, value):
        if value:
            if User.objects.filter(email=value).exists():
                self.fail('duplicate_email')
            else:
                return value
        return value
