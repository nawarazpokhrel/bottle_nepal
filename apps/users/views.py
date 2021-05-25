import jwt
from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users import usecases, serializers
from apps.users.models import SubscribeEmail
from bottle_nepal.settings import SECRET_KEY

User = get_user_model()


class CreateAPIView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.perform_create(serializer)
        return self.response(serializer=serializer, result=result, status_code=status.HTTP_201_CREATED)

    def response(self, serializer, result, status_code):
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status_code, headers=headers)


class RegisterUserView(CreateAPIView):
    """
    Use this to register user
    """
    serializer_class = serializers.RegisterUserSerializer
    permission_classes = (AllowAny,)

    # response_serializer_class = serializers.RegisterUserSerializer

    def perform_create(self, serializer):
        return usecases.RegisterUserUseCase(
            serializer=serializer,
            request=self.request
        ).execute()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'created':'User Created Check Your Email'}, status=status.HTTP_201_CREATED)


class VerifyEmailView(generics.GenericAPIView):
    """
    Use this to verify user email
    """
    serializer_class = None
    permission_classes = (AllowAny,)

    def get(self, request):
        # First get token from user browser
        token = request.GET.get('token')
        try:
            # decoding the token along with secret key
            payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
            # get the user that sent the payload
            user = User.objects.get(id=payload['user_id'])
            # now verify the user
            subscribe_email = SubscribeEmail(user=user)
            subscribe_email.save()
            return Response({'email': 'Successfully subscribed'}, status=status.HTTP_200_OK)
        # raise exceptions if token expired
        except jwt.ExpiredSignatureError as e:
            return Response({'error': 'Activations link expired'}, status=status.HTTP_400_BAD_REQUEST)
        # raise exception if the token sent is wrong
        except jwt.exceptions.DecodeError as e:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)