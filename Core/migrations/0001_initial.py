# Generated by Django 4.2 on 2022-06-16 03:53

import Core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Batches',
                'ordering': ['batch'],
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, validators=[Core.validators.branch_name_re()])),
                ('active', models.BooleanField(default=True)),
                ('code', models.IntegerField(validators=[Core.validators.branch_code_re()])),
            ],
            options={
                'verbose_name_plural': 'Branches',
            },
        ),
        migrations.CreateModel(
            name='FilerAdmin',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='filer.file')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('filer.file',),
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venue', models.CharField(max_length=20, validators=[Core.validators.branch_name_re()])),
                ('state', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('Auth.user',),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_no', models.CharField(max_length=11, primary_key=True, serialize=False, validators=[Core.validators.student_no_re()])),
                ('name', models.CharField(max_length=255, validators=[Core.validators.student_name_re()])),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Core.batch')),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Core.branch')),
            ],
        ),
        migrations.CreateModel(
            name='LateEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='late_entry', to='Core.student')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='late_entry', to='Core.venue')),
            ],
            options={
                'verbose_name_plural': 'Late Entries',
            },
        ),
        migrations.CreateModel(
            name='CustomImage',
            fields=[
                ('_height', models.FloatField(blank=True, null=True)),
                ('_width', models.FloatField(blank=True, null=True)),
                ('default_alt_text', models.CharField(blank=True, max_length=255, null=True, verbose_name='default alt text')),
                ('default_caption', models.CharField(blank=True, max_length=255, null=True, verbose_name='default caption')),
                ('subject_location', models.CharField(blank=True, default='', max_length=64, verbose_name='subject location')),
                ('file_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='%(app_label)s_%(class)s_file', serialize=False, to='filer.file')),
                ('batch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Core.batch')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_image', to='Core.student')),
            ],
            options={
                'verbose_name': 'image',
                'verbose_name_plural': 'images',
                'abstract': False,
                'default_manager_name': 'objects',
            },
            bases=('filer.file',),
        ),
        migrations.AddConstraint(
            model_name='batch',
            constraint=models.CheckConstraint(check=models.Q(('batch__gt', 1997)), name='check_batch'),
        ),
    ]
