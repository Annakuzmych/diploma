# Generated by Django 4.2 on 2023-05-17 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_remove_invitation_code_invitation_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='token',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
