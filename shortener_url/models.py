from django.db import models

class Url(models.Model):
    original_url = models.CharField(max_length=255)
    short_url = models.CharField(max_length=255)
    custom_alias = models.CharField(max_length=255)
    accesses = models.IntegerField(default=0)

    @property
    def new_access(self):
        self.accesses += 1
        self.save()
