# Generated by Django 4.0.4 on 2022-06-07 18:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_chapters_usercoursemapping_subjects_subchapters_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('question_image_file', models.FileField(blank=True, null=True, upload_to='Questions')),
                ('hint', models.CharField(max_length=1000, null=True)),
                ('hint_image', models.FileField(blank=True, null=True, upload_to='Qustion_hints')),
                ('solution', models.CharField(max_length=1000, null=True)),
                ('sol_image', models.FileField(blank=True, null=True, upload_to='Solutions')),
                ('difficulty_level', models.CharField(max_length=15, null=True)),
                ('type_of_question', models.CharField(max_length=20, null=True)),
                ('source', models.CharField(max_length=60, null=True)),
                ('weightage', models.IntegerField(null=True)),
                ('is_practice_test', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ScoreTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_time_stamp', models.DateTimeField(auto_created=True)),
                ('score_cumulative', models.FloatField(null=True)),
                ('attempt_no', models.IntegerField(null=True)),
                ('test_complete', models.BooleanField(default=False)),
                ('chapter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.chapters')),
                ('subchapter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.subchapters')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('thumbnailUrl', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_response', models.CharField(max_length=1000, null=True)),
                ('score', models.IntegerField(null=True)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.questions')),
                ('score_table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.scoretable')),
                ('user_profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='questions',
            name='topic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.topic'),
        ),
        migrations.CreateModel(
            name='AnswerOptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_options', models.CharField(max_length=200, null=True)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.questions')),
            ],
        ),
    ]
