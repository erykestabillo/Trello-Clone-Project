# Generated by Django 2.0.13 on 2019-10-14 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello', '0017_auto_20191014_1645'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boardmembers',
            options={'permissions': (('can_add_card', 'Can add card'), ('can_edit_card', 'Can edit card'))},
        ),
    ]