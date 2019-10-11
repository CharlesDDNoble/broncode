# Generated by Django 2.2.5 on 2019-09-26 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
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
                ('example_code', models.CharField(max_length=4096)),
                ('compiler_flags', models.CharField(max_length=512)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poc.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128)),
                ('completed_lessons', models.ManyToManyField(to='poc.Lesson')),
                ('courses', models.ManyToManyField(to='poc.Course')),
                ('owned', models.ManyToManyField(related_name='owned_courses', to='poc.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4096)),
                ('compiler_flags', models.CharField(max_length=512)),
                ('passed', models.BooleanField(default=False)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poc.Lesson')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poc.User')),
            ],
        ),
        migrations.CreateModel(
            name='SolutionSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stdin', models.CharField(max_length=2048)),
                ('stdout', models.CharField(max_length=2048)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poc.Lesson')),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poc.Course'),
        ),
    ]
