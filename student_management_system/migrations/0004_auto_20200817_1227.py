# Generated by Django 3.0.7 on 2020-08-17 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_system', '0003_notificationreceiver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='session_year_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_management_system.SessionYear'),
        ),
    ]