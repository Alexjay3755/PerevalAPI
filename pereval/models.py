from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=255)
    fam = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    otc = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Level(models.Model):
    winter = models.CharField(max_length=255, null=True)
    summer = models.CharField(max_length=255, null=True)
    autumn = models.CharField(max_length=255, null=True)
    spring = models.CharField(max_length=255, null=True)


class Pereval(models.Model):
    STATUS_CHOICES = (
        ("new", "новый"), ("pending", "в работе"),
        ("accepted", "принят"), ("rejected", "не принят")
    )
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.CharField(max_length=255, null=True, blank=True)
    add_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)


class Images(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name="images")
    data = models.URLField()
    title = models.CharField(max_length=255)


