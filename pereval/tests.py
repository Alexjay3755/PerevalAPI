import json
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Pereval, User, Level, Coords, Images
from pereval.serializers import PerevalSerializer


class PerevalAPITestCase(APITestCase):

    def setUp(self):
        self.pereval_1 = Pereval.objects.create(
            title="Тестовый перевал 1",
            beauty_title="Тестовый перевал 1",
            other_titles="Тестовый перевал 1",
            connect="connect...",
            add_time="2021-09-22T13:18:13Z",
            user=User.objects.create(
                email="email1@mail.ru",
                fam="fam-1",
                name="name-1",
                otc="otc-1",
                phone="89000000001"

            ),
            coords=Coords.objects.create(
                latitude=123.00,
                longitude=123.00,
                height=7890
            ),
            level=Level.objects.create(
                winter="1A",
                summer="1A",
                autumn="1A",
                spring="",
            )
        )
        self.image_1_1 = Images.objects.create(
            data="https://pereval.ru/image-1.jpg",
            title="title-1",
            pereval=self.pereval_1,
        )
        self.image_1_2 = Images.objects.create(
            data="https://pereval.ru/image-2.jpg",
            title="title-2",
            pereval=self.pereval_1,
        )

        self.pereval_2 = Pereval.objects.create(
            title="Тестовый перевал 2",
            beauty_title="Тестовый перевал 2",
            other_titles="Тестовый перевал 2",
            connect="",
            add_time="2021-09-22T13:18:13Z",
            status="pending",
            user=User.objects.create(
                email="email2@mail.ru",
                fam="fam-2",
                name="name-2",
                otc="otc-2",
                phone="89000000002"

            ),
            coords=Coords.objects.create(
                latitude=123.02,
                longitude=123.02,
                height=7892
            ),
            level=Level.objects.create(
                winter="",
                summer="1A",
                autumn="1A",
                spring="1A",
            )
        )
        self.image_2_1 = Images.objects.create(
            data="https://pereval.ru/image-3.jpg",
            title="title-1",
            pereval=self.pereval_2,
        )
        self.image_2_2 = Images.objects.create(
            data="https://pereval.ru/image-4.jpg",
            title="title-2",
            pereval=self.pereval_2,
        )

    def test_get_list(self):
        url = reverse('pereval-list')
        response = self.client.get(url)
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(2, len(serializer_data))

    def test_get_detail(self):
        url = reverse('pereval-detail', kwargs={'pk': self.pereval_1.pk})
        response = self.client.get(url)
        serializer_data = PerevalSerializer(self.pereval_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_not_create_pereval(self):
        url = reverse('pereval-list')
        data = {
            "title": "",
            "beauty_title": "Тестовый перевал 3",
            "other_titles": "Тестовый перевал 3",
            "connect": "",
            "add_time": "2021-09-22T13:18:13Z",
            "user": {
                "email": "email1@mail.ru",
                "fam": "fam-1",
                "name": "name-1",
                "otc": "otc-1",
                "phone": "89000000001"
            },
            "level": {
                "winter": "1B",
                "summer": "",
                "autumn": "1B",
                "spring": "1B"
            },
            "coords": {
                "latitude": 123.00,
                "longitude": 456.00,
                "height": 47896
            },
            "images": [
                {
                    "data": "https://pereval.ru/image-5.jpg",
                    "title": "заголовок 1"
                },
                {
                    "data": "https://pereval.ru/image-6.jpg",
                    "title": "заголовок 2"
                }
            ]
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(2, Pereval.objects.count())

    def test_create_pereval_exists_user(self):
        url = reverse('pereval-list')
        data = {
            "title": "Тестовый перевал 3",
            "beauty_title": "Тестовый перевал 3",
            "other_titles": "Тестовый перевал 3",
            "connect": "",
            "add_time": "2021-09-22T13:18:13Z",
            "user": {
                "email": "email1@mail.ru",
                "fam": "fam-1",
                "name": "name-1",
                "otc": "otc-1",
                "phone": "89000000001"
            },
            "level": {
                "winter": "1B",
                "summer": "",
                "autumn": "1B",
                "spring": "1B"
            },
            "coords": {
                "latitude": 123.00,
                "longitude": 456.00,
                "height": 47896
            },
            "images": [
                {
                    "data": "https://pereval.ru/image-5.jpg",
                    "title": "заголовок 1"
                },
                {
                    "data": "https://pereval.ru/image-6.jpg",
                    "title": "заголовок 2"
                }
            ]
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(3, Pereval.objects.count())
        self.assertEqual(2, User.objects.count())

    def test_update_pereval(self):
        url = reverse('pereval-detail', kwargs={'pk': self.pereval_1.pk})
        data = {
            "title": "Тестовый перевал 11",
            "beauty_title": "Тестовый перевал 111",
            "other_titles": "Тестовый перевал 1111",
            "connect": "",
            "add_time": "2021-09-22T13:18:13Z",
            "user": {
                "email": "email1@mail.ru",
                "fam": "fam-1",
                "name": "name-1",
                "otc": "otc-1",
                "phone": "89000000001"
            },
            "level": {
                "winter": "1B",
                "summer": "",
                "autumn": "1B",
                "spring": "1B"
            },
            "coords": {
                "latitude": 723.00,
                "longitude": 756.00,
                "height": 47896
            },
            "images": [
                {
                    "data": "https://pereval.ru/image-5.jpg",
                    "title": "заголовок 1"
                },
                {
                    "data": "https://pereval.ru/image-6.jpg",
                    "title": "заголовок 2"
                }
            ]
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.pereval_1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.pereval_1.title, "Тестовый перевал 11")
        self.assertEqual(self.pereval_1.beauty_title, "Тестовый перевал 111")
        self.assertEqual(self.pereval_1.other_titles, "Тестовый перевал 1111")
        self.assertEqual(self.pereval_1.coords.latitude, 723.00)
        self.assertEqual(self.pereval_1.coords.longitude, 756.00)

    def test_not_update_incorrect_status(self):
        url = reverse('pereval-detail', kwargs={'pk': self.pereval_2.pk})
        data = {
            "title": "Тестовый перевал 11",
            "beauty_title": "Тестовый перевал 111",
            "other_titles": "Тестовый перевал 1111",
            "connect": "",
            "add_time": "2021-09-22T13:18:13Z",
            "user": {
                "email": "email1@mail.ru",
                "fam": "fam-1",
                "name": "name-1",
                "otc": "otc-1",
                "phone": "89000000001"
            },
            "level": {
                "winter": "1B",
                "summer": "",
                "autumn": "1B",
                "spring": "1B"
            },
            "coords": {
                "latitude": 723.00,
                "longitude": 756.00,
                "height": 47896
            },
            "images": [
                {
                    "data": "https://pereval.ru/image-5.jpg",
                    "title": "заголовок 1"
                },
                {
                    "data": "https://pereval.ru/image-6.jpg",
                    "title": "заголовок 2"
                }
            ]
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.pereval_2.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(self.pereval_2.title, "Тестовый перевал 2")
        self.assertEqual(self.pereval_2.beauty_title, "Тестовый перевал 2")
        self.assertEqual(self.pereval_2.other_titles, "Тестовый перевал 2")
        self.assertEqual(self.pereval_2.coords.latitude, 123.02)
        self.assertEqual(self.pereval_2.coords.longitude, 123.02)

    def test_not_update_user_data_edit(self):
        url = reverse('pereval-detail', kwargs={'pk': self.pereval_1.pk})
        data = {
            "title": "Тестовый перевал 11",
            "beauty_title": "Тестовый перевал 111",
            "other_titles": "Тестовый перевал 1111",
            "connect": "",
            "add_time": "2021-09-22T13:18:13Z",
            "user": {
                "email": "email111@mail.ru",
                "fam": "fam-111",
                "name": "name-111",
                "otc": "otc-111",
                "phone": "89000000111"
            },
            "level": {
                "winter": "1B",
                "summer": "",
                "autumn": "1B",
                "spring": "1B"
            },
            "coords": {
                "latitude": 723.00,
                "longitude": 756.00,
                "height": 47896
            },
            "images": [
                {
                    "data": "https://pereval.ru/image-5.jpg",
                    "title": "заголовок 1"
                },
                {
                    "data": "https://pereval.ru/image-6.jpg",
                    "title": "заголовок 2"
                }
            ]
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.pereval_1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(self.pereval_1.title, "Тестовый перевал 1")
        self.assertEqual(self.pereval_1.beauty_title, "Тестовый перевал 1")
        self.assertEqual(self.pereval_1.other_titles, "Тестовый перевал 1")
        self.assertEqual(self.pereval_1.user.email, "email1@mail.ru")
        self.assertEqual(self.pereval_1.user.fam, "fam-1")
        self.assertEqual(self.pereval_1.user.name, "name-1")
        self.assertEqual(self.pereval_1.user.otc, "otc-1")
        self.assertEqual(self.pereval_1.user.phone, "89000000001")


class PerevalSerializerTestCase(TestCase):
    def setUp(self):
        self.pereval_1 = Pereval.objects.create(
            title="Тестовый перевал 1",
            beauty_title="Тестовый перевал 1",
            other_titles="Тестовый перевал 1",
            connect="connect...",
            add_time="2021-09-22T13:18:13Z",
            user=User.objects.create(
                email="email1@mail.ru",
                fam="fam-1",
                name="name-1",
                otc="otc-1",
                phone="89000000001"

            ),
            coords=Coords.objects.create(
                latitude=123.00,
                longitude=123.00,
                height=7890
            ),
            level=Level.objects.create(
                winter="1A",
                summer="1A",
                autumn="1A",
                spring="",
            )
        )
        self.image_1_1 = Images.objects.create(
            data="https://pereval.ru/image-1.jpg",
            title="title-1",
            pereval=self.pereval_1,
        )
        self.image_1_2 = Images.objects.create(
            data="https://pereval.ru/image-2.jpg",
            title="title-2",
            pereval=self.pereval_1,
        )

    def test_serializer_ok(self):
        data = PerevalSerializer([self.pereval_1], many=True).data
        expected_data = [
            {
                "title": "Тестовый перевал 1",
                "beauty_title": "Тестовый перевал 1",
                "other_titles": "Тестовый перевал 1",
                "connect": "connect...",
                "add_time": "2021-09-22T13:18:13Z",
                "status": "new",
                "user": {
                    "email": "email1@mail.ru",
                    "fam": "fam-1",
                    "name": "name-1",
                    "otc": "otc-1",
                    "phone": "89000000001"
                },
                "coords": {
                    "latitude": 123.00,
                    "longitude": 123.00,
                    "height": 7890
                },
                "level": {
                    "winter": "1A",
                    "summer": "1A",
                    "autumn": "1A",
                    "spring": ""
                },
                "images": [
                    {
                        "data": "https://pereval.ru/image-1.jpg",
                        "title": "title-1"
                    },
                    {
                        "data": "https://pereval.ru/image-2.jpg",
                        "title": "title-2"
                    }
                ]
            }
        ]
        self.assertEqual(data, expected_data)

