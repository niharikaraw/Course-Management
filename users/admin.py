from django.contrib import admin
from users.models import ChapterNotes, Chapters, Courses, CustomUser, Subchapters, Subjects, TeacherProfile, Topics, UserCourseMapping

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Courses)
admin.site.register(UserCourseMapping)
admin.site.register(Subjects)
admin.site.register(Chapters)
admin.site.register(Subchapters)
admin.site.register(ChapterNotes)
admin.site.register(TeacherProfile)
admin.site.register(Topics)