# Generated by Django 3.2.20 on 2023-08-06 19:57

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import opaque_keys.edx.django.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('usage_key', opaque_keys.edx.django.models.UsageKeyField(max_length=255, primary_key=True, serialize=False)),
                ('display_name', models.CharField(max_length=255)),
                ('sequence', models.SmallIntegerField(default=0)),
            ],
            options={
                'ordering': ('course', 'sequence'),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', opaque_keys.edx.django.models.CourseKeyField(max_length=255, primary_key=True, serialize=False)),
                ('org', models.CharField(db_index=True, editable=False, max_length=255)),
                ('number', models.CharField(db_index=True, editable=False, max_length=255)),
                ('run', models.CharField(db_index=True, editable=False, max_length=255)),
                ('display_name', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('invitation_only', models.BooleanField(blank=True, null=True)),
                ('course_image_url', models.URLField(blank=True, max_length=1000, null=True)),
                ('effort', models.CharField(blank=True, max_length=20, null=True)),
                ('visible_to_staff_only', models.BooleanField(blank=True, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('enrollment_start', models.DateTimeField(blank=True, null=True)),
                ('enrollment_end', models.DateTimeField(blank=True, null=True)),
                ('certificate_available_date', models.DateTimeField(blank=True, null=True)),
                ('pacing', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'unique_together': {('org', 'number', 'run')},
            },
        ),
        migrations.CreateModel(
            name='Subsection',
            fields=[
                ('usage_key', opaque_keys.edx.django.models.UsageKeyField(max_length=255, primary_key=True, serialize=False)),
                ('display_name', models.CharField(max_length=255)),
                ('sequence', models.SmallIntegerField(default=0)),
                ('format', models.CharField(blank=True, max_length=50, null=True)),
                ('lms_web_url', models.URLField(max_length=1000)),
                ('student_view_url', models.URLField(max_length=1000)),
                ('is_special_exam', models.BooleanField(default=False)),
                ('weight', models.FloatField(default=0)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.chapter')),
            ],
            options={
                'ordering': ('chapter', 'sequence'),
            },
        ),
        migrations.AddField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('usage_key', opaque_keys.edx.django.models.UsageKeyField(max_length=255, primary_key=True, serialize=False)),
                ('block_type', models.CharField(db_index=True, max_length=100)),
                ('display_name', models.CharField(max_length=255)),
                ('lms_web_url', models.URLField(max_length=1000)),
                ('student_view_url', models.URLField(max_length=1000)),
                ('subsection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.subsection')),
            ],
        ),
        migrations.CreateModel(
            name='CourseAccessRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('org', models.CharField(blank=True, db_index=True, max_length=64, null=True)),
                ('role', models.CharField(db_index=True, max_length=64)),
                ('deleted', models.BooleanField(blank=True, null=True)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
            options={
                'unique_together': {('student', 'org', 'course_id', 'role')},
            },
        ),
    ]
