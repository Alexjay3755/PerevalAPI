from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response



def incorrect_user_data(user_data, user_dict):
    return user_data and user_data != user_dict


def incorrect_status_response(pereval):
    return Response(
        {"state": 0, "message": f"Некорректный статус: '{pereval.get_status_display()}'"},
        status=status.HTTP_409_CONFLICT
    )


def not_edit_user_response():
    return Response(
        {"state": 0, "message": "Данные пользователя изменять нельзя!"},
        status=status.HTTP_409_CONFLICT
    )


def update_ok_response():
    return Response(
        {"state": 1, "message": "Перевал успешно обновлен"},
        status=status.HTTP_200_OK
    )

def create_ok_response(serializer):
    return Response(
        {"status": 200, "message": None, "id": serializer.instance.id},
        status=status.HTTP_200_OK
    )

def bad_request_response(serializer):
    return Response(
        {"status": 400, "message": serializer.errors, "id": None},
        status=status.HTTP_400_BAD_REQUEST
    )

def database_error_response(e):
    return Response(
        {"status": 500, 'message': f"Ошибка подключения к базе данных: {str(e)}", "id": None},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )