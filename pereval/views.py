from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.db import DatabaseError
from .models import User,Coords, Level, Images, Pereval
from .serializers import (
    UserSerializer, CoordsSerializer, LevelSerializer,
    ImagesSerializer, PerevalSerializer
)


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


    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        serializer = self.get_serializer(pereval, data=request.data, partial=True)
        if pereval.status != "new":
            return Response(
                {"state": 0, "message": f"Некорректный статус: <>{pereval.get_status_display()}<>"},
                status=status.HTTP_409_CONFLICT
            )
        user_dict = model_to_dict(pereval.user)
        user_dict.pop("id")
        if request.data.get("user") and request.data.get("user") != user_dict:
            return Response(
                {"state": 0, "message": "Данные пользователя измениять нельзя!"},
                status=status.HTTP_409_CONFLICT
            )

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"state": 1, "message": "Перевал успешно обновлён"},
            status=status.HTTP_200_OK
        )




