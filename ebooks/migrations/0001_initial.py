# Generated by Django 4.1.3 on 2022-11-12 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('cover', models.ImageField(upload_to='')),
                ('book', models.FileField(upload_to='')),
                ('bookaudio', models.FileField(upload_to='')),
            ],
        ),
    ]
