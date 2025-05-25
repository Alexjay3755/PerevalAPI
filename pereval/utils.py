from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response


def check_unique_model_data(data, model, fields):
    for field in fields:
        model_data = data.copy()
        model_data_field = model_data.pop(field)
        filter_kwargs = {field: model_data_field}
        model_obj = model.objects.filter(**filter_kwargs).first()
        if model_obj:
            model_dict = model_to_dict(model_obj)
            model_dict.pop(field)
            model_dict.pop("id")
            if model_data != model_dict:
                return False, field
    return True, None


def check_unique_model_data_response(field):
    return Response(
        {"status": 409, "message": f"Этот {field} уже занят другим пользователем"},
        status=status.HTTP_200_OK
    )




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