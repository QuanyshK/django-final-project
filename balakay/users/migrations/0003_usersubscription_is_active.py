# Generated by Django 5.1.2 on 2024-10-30 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_client_alter_child_parent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]