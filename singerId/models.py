from django.db import models


class SingerId(models.Model):
    singer = models.CharField(max_length=255)
    singername = models.CharField(max_length=255)
    commentator = models.CharField(max_length=255)

    class Meta:
        app_label = 'singerId'
        db_table = 'sing_id'
