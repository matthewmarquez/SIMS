# Generated by Django 2.1.7 on 2019-02-17 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simslounge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resident',
            name='resident_title',
            field=models.CharField(default='this', max_length=200),
            preserve_default=False,
        ),
    ]