# Generated by Django 3.0.7 on 2020-07-09 09:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=150, null=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('username', models.CharField(blank=True, max_length=30, null=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[(1, 'HOD'), (2, 'Staff'), (3, 'Students'), (4, 'Parents')], default=1, max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_date', models.DateField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('receiver', models.CharField(max_length=20)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=12)),
                ('profile_Image', models.ImageField(blank=True, default='default.jpg', upload_to='profile-pic')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SessionYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_start_year', models.DateField()),
                ('session_end_year', models.DateField()),
                ('term', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=20)),
                ('phone_number', models.CharField(max_length=12)),
                ('profile_Image', models.ImageField(default='default.jpg', upload_to='profile-pic')),
                ('current_position', models.CharField(max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('grade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_management_system.Class')),
                ('subject_teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_management_system.Staff')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=20)),
                ('profile_Image', models.ImageField(default='default.jpg', upload_to='profile-pic')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('grade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_management_system.Class')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_management_system.Parent')),
            ],
        ),

        migrations.CreateModel(
            name='FeedbackStudents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.TextField()),
                ('feedback_reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_system.Student')),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackStaff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.CharField(max_length=200)),
                ('feedback_reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_system.Staff')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='form_master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_management_system.Staff'),
        ),
        migrations.AddField(
            model_name='class',
            name='session_year_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_system.SessionYear'),
        ),
        migrations.CreateModel(
            name='AttendanceReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attendance_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_system.Attendance')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_system.Student')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='class_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_management_system.Class'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='session_year_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_system.SessionYear'),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
