from django.db import DatabaseError
from django.forms.models import model_to_dict
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from pereval.models import User, Coords, Level, Pereval, Images
from pereval.serializers import (
    UserSerializer, CoordsSerializer, LevelSerializer,
    PerevalSerializer, ImagesSerializer
)
from .utils import (
    incorrect_status_response, not_edit_user_response,
    incorrect_user_data, update_ok_response, bad_request_response, create_ok_response, database_error_response,
    check_unique_model_data, check_unique_model_data_response
)
from .yasg import user_email, example_pereval, pereval_status, user_fam

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get',]
    filterset_fields = ('fam',)

    @swagger_auto_schema(manual_parameters=[user_fam], )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CoordsViewSet(ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer


class LevelViewSet(ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImagesViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class PerevalViewSet(ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    http_method_names = ['get', 'post', 'patch']
    filterset_fields = ('user__email', 'status')

    @swagger_auto_schema(request_body=example_pereval)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user_data = request.data.get('user')
        fields = ["email", "phone"]
        check_unique_model, field = check_unique_model_data(user_data, User, fields)
        if not check_unique_model:
            return check_unique_model_data_response(field)
        try:
            if not serializer.is_valid():
                return bad_request_response(serializer)
            serializer.save()
            return create_ok_response(serializer)
        except DatabaseError as e:
            return database_error_response(e)

    @swagger_auto_schema(request_body=example_pereval)
    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        serializer = self.get_serializer(pereval, data=request.data, partial=True)

        if pereval.status != "new":
            return incorrect_status_response(pereval)

        user_dict = model_to_dict(pereval.user)
        user_dict.pop('id')
        user_data = request.data.get("user")
        if incorrect_user_data(user_data, user_dict):
            return not_edit_user_response()

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return update_ok_response()

    @swagger_auto_schema(manual_parameters=[user_email, pereval_status], )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
