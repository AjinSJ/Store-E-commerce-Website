# Generated by Django 5.0 on 2024-10-14 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mittais', '0008_newlaunch_topbrands'),
    ]

    operations = [
        migrations.AddField(
            model_name='newlaunch',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]