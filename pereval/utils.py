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


def ok_response():
    return Response(
        {"state": 1, "message": "Перевал успешно обновлен"},
        status=status.HTTP_200_OK
    )
