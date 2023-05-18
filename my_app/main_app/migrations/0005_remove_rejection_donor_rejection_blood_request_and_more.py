# Generated by Django 4.2 on 2023-05-16 11:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_remove_bloodrequest_approving_doctor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rejection',
            name='donor',
        ),
        migrations.AddField(
            model_name='rejection',
            name='blood_request',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main_app.bloodrequest'),
        ),
        migrations.AlterField(
            model_name='bloodrequest',
            name='donation_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='bloodrequest',
            name='donor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blood_requests', to='main_app.donor'),
        ),
    ]
