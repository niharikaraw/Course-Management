
from cgitb import text
from imp import source_from_cache
from operator import truediv
from pydoc_data.topics import topics
from pyexpat import model
from tkinter import CASCADE
from turtle import title
from urllib import response
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUser(AbstractUser):
    mobile_number = models.CharField(max_length=15, null=True)
    grade = models.IntegerField(null=True)
    selection_of_exams = models.CharField(max_length=50, null=True)
    preffered_lang = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=15, null=True)
    device_id = models.CharField(max_length=50, null=True)
    profile_pic = models.FileField(null=True, upload_to='profile_pic', blank=True)

    def __str__(self):
        return str(self.first_name)


class TeacherProfile(models.Model):
    name = models.CharField(max_length=50, null=True)
    profile_pic = models.FileField(null=True, blank=True, upload_to='Teacher_profile_pic')

    def __str__(self):
        return str(self.name)


class Courses(models.Model):
    title = models.CharField(max_length=60)
    thumbnail = models.FileField(null=True, blank=True, upload_to='Course_thumbnails')
    overview = models.CharField(max_length=200, null=True)
    price = models.IntegerField(null=True)

    def __str__(self):
        return str(self.title)


class Subjects(models.Model):
    title = models.CharField(max_length=20)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.title)


class Chapters(models.Model):
    title = models.CharField(max_length=60)
    number_of_subchapters = models.IntegerField(null=True)
    notes = models.FileField(null=True, blank=True, upload_to='Chapter_notes')
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.title)


class Subchapters(models.Model):
    title = models.CharField(max_length=60)
    number_of_topics = models.IntegerField(null=True)
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.title)


class Topics(models.Model):
    title = models.CharField(max_length=60)
    thumbnailUrl = models.CharField(max_length=50, null=True, blank=True)
    subchapter = models.ForeignKey(Subchapters, on_delete=models.CASCADE, null=True)
    video = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.title)


class Questions(models.Model):
    title = models.CharField(max_length=60)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, null= True)
    question_image_file = models.FileField(null=True, blank=True, upload_to='Questions')
    hint = models.CharField(max_length=1000, null=True)
    hint_image = models.FileField(null=True, blank=True, upload_to='Qustion_hints')
    solution = models.CharField(max_length=1000, null=True)
    sol_image = models.FileField(null=True, blank=True, upload_to='Solutions')
    difficulty_level = models.CharField(max_length=15, null=True)
    type_of_question = models.CharField(max_length=20, null=True)
    source = models.CharField(max_length=60, null=True)
    weightage = models.IntegerField(null=True)
    is_practice_test = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)


class AnswerOptions(models.Model):
    answer_options = models.CharField(max_length=200, null=True)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True)


class ScoreTable(models.Model):
    score_cumulative = models.FloatField(null=True)
    attempt_no = models.IntegerField(null=True)
    attempt_time_stamp = models.DateTimeField(auto_created=True)
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE, null=True)
    subchapter = models.ForeignKey(Subchapters, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    test_complete = models.BooleanField(default=False)


class UserResponse(models.Model):
    question =models.ForeignKey(Questions, on_delete=models.CASCADE, null=True)
    user_profile = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    answer_response = models.CharField(max_length=1000, null=True)
    score = models.IntegerField(null=True)
    score_table = models.ForeignKey(ScoreTable, on_delete=models.CASCADE, null=True)


class LiveClasses(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)
    teacher_profile = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200, null=True)
    videoUrl = models.CharField(max_length=70, null=True)
    thumbnail = models.FileField(null=True, blank=True, upload_to='LiveClassThumbnail')
    class_date = models.DateField(null=True, blank=True)
    class_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.title)


class Gyan(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=60, null=True)
    image = models.FileField(null=True, blank=True, upload_to='GyanImages')
    description = models.CharField(max_length=100, null=True)
    file = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.title)


class ChapterNotes(models.Model):
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE, null=True)
    file_url = models.URLField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.chapter)

class TopicsCovered(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, null=True)
    time_stamp = models.DateTimeField(auto_created=True)

    def __str__(self):
        return str(self.topic)


class ProgressReportSubChap(models.Model):
    sub_chapter = models.ForeignKey(Subchapters, on_delete=models.CASCADE, null=True)
    latest_attempt = models.ForeignKey(ScoreTable, on_delete=models.CASCADE, null=True, related_name='SubChapter_progress_latest_attempt')
    lowest_attempt = models.ForeignKey(ScoreTable, on_delete=models.CASCADE, null=True)
    highest_attempt = models.ForeignKey(ScoreTable, on_delete=models.CASCADE, null=True, related_name='SubChapter_progress_highest_attempt')
    total_attempts = models.IntegerField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)


class ProgressReportChap(models.Model):
    chapter = models.ForeignKey(Chapters, on_delete=models.CASCADE, null=True)
    latest_attempt = models.ForeignKey(ScoreTable, on_delete=models.CASCADE, null=True, related_name='Chapter_progress_latest_attempt')
    lowest_attempt = models.ForeignKey(ScoreTable, on_delete=models.CASCADE, null=True)
    highest_attempt = models.ForeignKey(ScoreTable, on_delete=models.CASCADE, null=True, related_name='Chapter_progress_highest_attempt')
    total_attempts = models.IntegerField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)


class Coupons(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    coupon_code = models.CharField(max_length=10, null=True)
    redeem_count = models.IntegerField(null=True)
    discount = models.FloatField(null=True)


class Transactions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    tansaction_ids = models.IntegerField(null=True)
    transaction_date = models.DateField(null=True, blank=True)
    transaction_time = models.TimeField(null=True, blank=True)
    amount = models.FloatField(null=True)
    mode_of_payment =models.CharField(max_length=20, null=True)


class UserCourseMapping(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True)