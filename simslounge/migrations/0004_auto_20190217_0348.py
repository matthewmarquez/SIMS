# Generated by Django 2.1.7 on 2019-02-17 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simslounge', '0003_auto_20190217_0345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposal',
            name='proposal_no',
            field=models.ManyToManyField(blank=True, null=True, related_name='no_votes', to='simslounge.LoungeMember'),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='proposal_yes',
            field=models.ManyToManyField(blank=True, null=True, related_name='yes_votes', to='simslounge.LoungeMember'),
        ),
    ]
