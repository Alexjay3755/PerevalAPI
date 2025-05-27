from drf_yasg import openapi

user_email = openapi.Parameter(
    'user__email', openapi.IN_QUERY,
    description="Поиск перевалов по электронной почте пользователя",
    type=openapi.TYPE_STRING
)

pereval_status = openapi.Parameter(
    'status', openapi.IN_QUERY,
    description="Поиск перевалов по статусу",
    type=openapi.TYPE_STRING
)

user_fam = openapi.Parameter(
    'fam', openapi.IN_QUERY,
    description="Поиск перевалов по статусу",
    type=openapi.TYPE_STRING
)


user_name = openapi.Parameter(
    'name', openapi.IN_QUERY,
    description="Поиск пользователей по имени",
    type=openapi.TYPE_STRING
)


example_pereval = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING, example="Горный перевал"),
        'beauty_title': openapi.Schema(type=openapi.TYPE_STRING, example="Супер перевал"),
        "other_titles": openapi.Schema(type=openapi.TYPE_STRING, example="Горный перевал Алтая"),
        "connect": openapi.Schema(type=openapi.TYPE_STRING, example="Соединяет..."),
        'add_time': openapi.Schema(type=openapi.FORMAT_DATETIME, example='2021-09-22T13:18:13Z'),
        'user': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, example='user@example.com'),
                'fam': openapi.Schema(type=openapi.TYPE_STRING, example='Иванов'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, example='Иван'),
                'otc': openapi.Schema(type=openapi.TYPE_STRING, example='Иванович'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, example='89991234567'),
            }
        ),
        'coords': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, example=42.1234),
                'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, example=75.5678),
                'height': openapi.Schema(type=openapi.TYPE_INTEGER, example=1500),
            }
        ),
        'level': openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'winter': openapi.Schema(type=openapi.TYPE_STRING, example='1A'),
                'summer': openapi.Schema(type=openapi.TYPE_STRING, example='1B'),
                'autumn': openapi.Schema(type=openapi.TYPE_STRING, example='1C'),
                'spring': openapi.Schema(type=openapi.TYPE_STRING, example='1D'),
            }
        ),
        'images': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'data': openapi.Schema(type=openapi.TYPE_STRING,
                                           example='https://mountain-passes.com/pereval-1.jpg'),
                    'title': openapi.Schema(type=openapi.TYPE_STRING, example='Вид на вершину')
                }
            )
        ),
    }
)