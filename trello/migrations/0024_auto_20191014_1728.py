# Generated by Django 2.0.13 on 2019-10-14 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trello', '0023_auto_20191014_1725'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='boardmembers',
            options={'permissions': (('can_add_card', 'Can add card'), ('can_edit_card', 'Can edit card'))},
        ),
        migrations.AlterModelOptions(
            name='trellouser',
            options={},
        ),
    ]