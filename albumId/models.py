from django.db import models


class AlbumId(models.Model):
    albumid = models.CharField(max_length=255)
    singer = models.CharField(max_length=255)
    albumname = models.CharField(max_length=255)
    albumpic = models.CharField(max_length=255)

    class Meta:
        app_label = 'albumId'
        db_table = 'album_Id'
