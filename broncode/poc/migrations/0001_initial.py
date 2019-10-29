# Generated by Django 2.2.5 on 2019-10-16 01:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('number', models.IntegerField()),
                ('markdown', models.TextField()),
                ('example_code', models.TextField()),
                ('compiler_flags', models.CharField(blank=True, max_length=512)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='poc.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=128)),
                ('last_name', models.CharField(default='', max_length=128)),
                ('email', models.EmailField(default='', max_length=254)),
                ('completed_lessons', models.ManyToManyField(blank=True, to='poc.Lesson')),
                ('enrolled_in', models.ManyToManyField(blank=True, to='poc.Course')),
                ('owned_courses', models.ManyToManyField(blank=True, related_name='owners', to='poc.Course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('compiler_flags', models.CharField(blank=True, max_length=512)),
                ('passed', models.BooleanField(default=False)),
                ('log', models.TextField(blank=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='poc.Lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='poc.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='poc.Course'),
        ),
        migrations.CreateModel(
            name='SolutionSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('stdin', models.TextField()),
                ('stdout', models.TextField()),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solution_sets', to='poc.Lesson')),
            ],
            options={
                'unique_together': {('lesson', 'number')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='chapter',
            unique_together={('course', 'number')},
        ),
    ]