# Generated by Django 2.2.6 on 2019-10-30 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_url_custom'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='url',
            constraint=models.UniqueConstraint(condition=models.Q(custom=False), fields=('short_url',), name='unique_random_url'),
        ),
    ]
