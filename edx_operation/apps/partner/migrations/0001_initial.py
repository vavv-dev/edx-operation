# Generated by Django 3.2.20 on 2023-08-06 19:57

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import edx_operation.apps.partner.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('uuid', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('slug', models.SlugField(max_length=30, unique=True)),
                ('active', models.BooleanField(blank=True, null=True)),
                ('size', models.CharField(blank=True, choices=[('large', '대기업'), ('middle', '중견기업'), ('small', '우선지원기업')], max_length=255, null=True)),
                ('phone', models.CharField(blank=True, help_text='ex) 02-1234-1234', max_length=50, null=True)),
                ('fax', models.CharField(blank=True, help_text='ex) 02-1234-1234', max_length=50, null=True)),
                ('management_number', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('id_number', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('ceo_name', models.CharField(blank=True, help_text='ex) 홍길동', max_length=50, null=True)),
                ('postal_code', models.CharField(blank=True, help_text='ex) 12345', max_length=10, null=True)),
                ('address', models.CharField(blank=True, help_text='ex) 서울시 서초구...', max_length=254, null=True)),
                ('secondary_key', models.CharField(blank=True, default=edx_operation.apps.partner.models.random_digits, max_length=16, null=True)),
            ],
            options={
                'verbose_name': 'Partner Customer',
                'verbose_name_plural': 'Partner Customers',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('domain', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PartnerStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('active', models.BooleanField(default=True)),
                ('linked', models.BooleanField(default=True)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.partner')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
            options={
                'verbose_name': 'Partner Student',
                'verbose_name_plural': 'Partner Students',
                'unique_together': {('partner', 'student')},
            },
        ),
        migrations.AddField(
            model_name='partner',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='partner.site'),
        ),
        migrations.AddField(
            model_name='partner',
            name='students',
            field=models.ManyToManyField(through='partner.PartnerStudent', to='student.Student'),
        ),
        migrations.CreateModel(
            name='PartnerEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('saved_for_later', models.BooleanField(blank=True, null=True)),
                ('unenrolled', models.BooleanField(blank=True, db_index=True, null=True)),
                ('unenrolled_at', models.DateTimeField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('partner_student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='partner.partnerstudent')),
            ],
            options={
                'verbose_name': 'Partner Enrollment',
                'verbose_name_plural': 'Partner Enrollments',
                'unique_together': {('partner_student', 'course')},
            },
        ),
    ]
