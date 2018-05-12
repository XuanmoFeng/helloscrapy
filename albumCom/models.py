from django.db import models

class AlbumComent(models.Model):
    albumid= models.CharField(max_length=255)
    comment= models.CharField(max_length=255)
    commentator=models.CharField(max_length=255)

    class Meta:
        app_label = 'albumCom'
        db_table = 'album_comment'