# Generated by Django 4.2 on 2023-05-23 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_statistics_bloodrequest_is_confirmed_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='blood_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='donation', to='main_app.bloodrequest'),
        ),
    ]
