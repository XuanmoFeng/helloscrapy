# Generated by Django 2.0.4 on 2018-04-20 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlbumComent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('albumid', models.CharField(max_length=255)),
                ('comment', models.CharField(max_length=255)),
                ('commentator', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'album_comment',
            },
        ),
    ]
