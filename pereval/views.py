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
from .utils import incorrect_status_response, not_edit_user_response, incorrect_user_data, ok_response
from .yasg import user_email, example_pereval, pereval_status

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
        try:
            if not serializer.is_valid():
                return Response(
                    {"status": 400, "message": serializer.errors, "id": None},
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(
                {"status": 200, "message": None, "id": serializer.instance.id},
                status=status.HTTP_200_OK
            )
        except DatabaseError as e:
            return Response(
                {"status": 500, 'message': f"Ошибка подключения к базе данных: {str(e)}", "id": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
        return ok_response()

    @swagger_auto_schema(manual_parameters=[user_email, pereval_status], )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
