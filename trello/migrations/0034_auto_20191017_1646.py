# Generated by Django 2.0.13 on 2019-10-17 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trello', '0033_auto_20191017_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardchecklist',
            name='checklist',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
