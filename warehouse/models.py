from django.db import models

class TestScrapy(models.Model):
    url= models.CharField(max_length=255)
    name= models.CharField(max_length=255)

    class Meta:
        app_label = 'warehouse'
        db_table = 'test_scrapy'
