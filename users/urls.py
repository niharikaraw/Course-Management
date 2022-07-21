from django.urls import path
from users.models import   Courses
from users.views import ChapterNotesView, ChapterView, CreateUserView, GetCourses, ProfleView, CourseMappingView, QuestionSetView, SubChapterView, SubjectView, TeachersView, TopicsView

urlpatterns = [
    path ('user-view/', CreateUserView.as_view(), name='user-view'),
    path ('courses-list/', GetCourses.as_view() , name='courses-list'),
    path ('user-profile/', ProfleView.as_view(), name='user-profile'),
    path ('user-course-mapping/', CourseMappingView.as_view(), name='user-course-mapping'),
    path ('subject-list/', SubjectView.as_view(), name='subject-list'),
    path ('chapter-list/', ChapterView.as_view(), name='chapter-list'),
    path ('subchapter-list/', SubChapterView.as_view(), name='subchapter-list'),
    path ('chapter-notes/', ChapterNotesView.as_view(), name='chapter-notes'),
    path ('teacher-list/', TeachersView.as_view(), name='teacher-list'),
    path ('topic-list/', TopicsView.as_view(), name='topic-list'),
    path ('question/', QuestionSetView.as_view(), name='question')
]