from rest_framework import serializers

from pereval.models import User, Coords, Level, Images, Pereval



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'fam', 'name', 'otc', 'phone')


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ('latitude', 'longitude', 'height')


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('winter', 'summer', 'autumn', 'spring')


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('data', 'title')


class PerevalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pereval
        fields = (
            'beauty_title', 'title', 'other_titles', 'connect',
            'add_time', 'status', 'user', 'level', 'coords', 'images'
        )




