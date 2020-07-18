# Generated by Django 3.0.7 on 2020-07-09 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='name',
            field=models.CharField(max_length=20),
        ),
        migrations.CreateModel(
            name='StudentResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_test', models.FloatField(null=True)),
                ('second_test', models.FloatField(null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('session_year_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_system.SessionYear')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_system.Student')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_system.Subject')),
            ],
        ),
    ]