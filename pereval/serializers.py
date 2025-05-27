from rest_framework import serializers

from pereval.models import User, Coords, Level, Images, Pereval
from drf_writable_nested.serializers import WritableNestedModelSerializer


class UserSerializer(WritableNestedModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'fam', 'name', 'otc', 'phone')


class CoordsSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Coords
        fields = ('latitude', 'longitude', 'height')


class LevelSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Level
        fields = ('winter', 'summer', 'autumn', 'spring')


class ImagesSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Images
        fields = ('data', 'title')


class PerevalSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    level = LevelSerializer()
    coords = CoordsSerializer()
    images = ImagesSerializer(many=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Pereval
        fields = (
            'beauty_title', 'title', 'other_titles', 'connect',
            'add_time', 'status', 'user', 'level', 'coords', 'images'
        )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        level_data = validated_data.pop('level')
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('images')

        user, _ = User.objects.get_or_create(**user_data)
        level = Level.objects.create(**level_data)
        coords = Coords.objects.create(**coords_data)

        pereval = Pereval.objects.create(user=user, level=level, coords=coords, **validated_data)

        for image_data in images_data:
            Images.objects.create(pereval=pereval, **image_data)

        return pereval




