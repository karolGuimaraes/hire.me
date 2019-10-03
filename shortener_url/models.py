from django.db import models

class Url(models.Model):
    original_url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=255)
    custom_alias = models.CharField(max_length=255)
