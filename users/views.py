from cgitb import text
from ctypes.wintypes import HINSTANCE
from imp import source_from_cache
import json
from turtle import title
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from requests import request
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from users.models import AnswerOptions, ChapterNotes, Chapters, CustomUser, Courses, LiveClasses, Questions, Subchapters, Subjects, TeacherProfile, Topics, UserCourseMapping
from rest_framework.permissions import IsAuthenticated



class CreateUserView(APIView):

    def post(self, request):
            data = request.data
            print(data)
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = make_password(data.get('password'))
            mobile_number = data.get('mobile_number')
            grade = data.get('grade')
            selection_of_exams = data.get('selection_of_exams')
            preffered_lang = data.get('preffered_lang')
            city = data.get('city')
            device_id = data.get('device_id')
            profile_pic = data.get('profile_pic')

            print(first_name,email,mobile_number,selection_of_exams,preffered_lang)
            if not (first_name and email and mobile_number and selection_of_exams and preffered_lang):
                return HttpResponse('Invalid body passed!')
            
            user = CustomUser(
                first_name = first_name, 
                last_name = last_name,
                email = email,
                password = password,
                username = email,
                mobile_number = mobile_number, 
                grade = grade, 
                selection_of_exams = selection_of_exams,
                preffered_lang = preffered_lang,
                city = city,
                device_id = device_id,
                profile_pic = profile_pic
            )
            
            user.save()
            return Response({'message':'User added successfully!'})


class GetCourses(APIView):
  
    def get(self, request):
        
            params = request.GET
            print(params)

            title = params.get("title")
            overview = params.get("overview")
            price = params.get("price")

            courses = Courses.objects.filter()

            if title:
                courses = courses.filter(title__icontains=title)
            if overview:
                courses = courses.filter(overview__icontains=overview)
                print(courses.query)
            if price:
                courses = courses.filter(price__lte=price)
            courses = list(courses.values())


            return Response({'data': courses})


class ProfleView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = model_to_dict(request.user)
        courses = UserCourseMapping.objects.filter(user=request.user).select_related('course')
        course_list = []
        for i in courses:
           x = model_to_dict(i.course)
           if x.get('thumbnail'):
               x['thumbnail'] = x.get('thumbnail').url
           else:
               x['thumbnail'] = None
           course_list.append(x)
        user['selected_courses'] = course_list
        
        print(user)
        if user.get('profile_pic'):
            user['profile_pic'] = user.get('profile_pic').url
        else:
            user['profile_pic'] = None
        del user['password']
        del user['last_login']
        del user['is_superuser']
        del user['is_staff']
        del user['is_active']
        del user['groups']
        del user['user_permissions']
        del user['device_id']
        del user['date_joined']


        return Response({"data": user})


    def patch(self, request):
        data = request.data
        user = request.user
        if data.get('first_name'):
            user.first_name = data.get('first_name')
        if data.get('last_name'):
            user.last_name = data.get('last_name')
        if data.get('mobile_number'):
            user.mobile_number = data.get('mobile_number')
        if data.get('city'):
            user.city = data.get('city')
        if data.get('selection_of_exams'):
            user.selection_of_exams = data.get('selection_of_exams')
        if data.get('preffered_lang'):
            user.preffered_lang = data.get('preffered_lang')
        if data.get('profile_pic'):
            user.profile_pic = data.get('profile_pic')
        user.save()
        user_obj = model_to_dict(request.user)
        if user.profile_pic:
            user_obj['profile_pic'] = user_obj.get('profile_pic').url
        else:
            user_obj['profile_pic'] = None
        del user_obj['password']
        del user_obj['last_login']
        del user_obj['is_superuser']
        del user_obj['is_staff']
        del user_obj['is_active']
        del user_obj['groups']
        del user_obj['user_permissions']
        del user_obj['device_id']
        del user_obj['date_joined']
        return Response({'data': user_obj})


class CourseMappingView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        user = request.user
        course_id = str(request.data.get('course_id'))
        print(course_id)
        if not course_id.isdigit():
            return Response({'message': 'Course ID missing or invalid'})
        try:
            user_course_mapping = UserCourseMapping(user=user, course_id=course_id)
            user_course_mapping.save()
        except Exception as e:
            return Response({'error': str(e)})

        return Response({'message': 'User-Course mapped successfully'})


class SubjectView(APIView):
    
    def get(self, request):
        data = request.GET
        print(data)
        cid = str(data.get('course_id'))
        print(cid.isdigit(),cid)
        if cid.isdigit():
            subject = Subjects.objects.filter(course_id=cid).values()
            print(subject)
            return Response({'data': subject})
        return Response({'message': 'No course ID passed'})


class ChapterView(APIView):
   
    def get(self,request):
        data = request.GET
        print(data)
        cid = str(data.get('course_id'))
        subject_id = str(data.get('subject_id'))
        print(cid)
        chap_id = str(data.get('chapter_id'))
        title = data.get('title')
        if subject_id.isdigit():
            chapter = Chapters.objects.filter(subject_id=subject_id).values()
            return Response({'data': chapter})
        if cid.isdigit():
            chapter = Chapters.objects.filter(subject__course_id=cid).values()
            return Response({'data': chapter})
        if chap_id.isdigit():
            chapter = Chapters.objects.filter(id=chap_id).values()
            return Response({'data': chapter})
        if title:
            chapter =  Chapters.objects.filter(title__icontains=title).values()
            return Response({'data': chapter})
        return Response({'message': 'Please provide correct input'})


class ChapterNotesView(APIView):
    
    def get(self, request):
        data = request.GET
        print(data)
        chap_id = str(data.get('chapter_id'))
        title = data.get('title')
        result = []
        chapter_notes = []
        if chap_id.isdigit():
            chapter_notes = ChapterNotes.objects.filter(chapter_id=chap_id)
            #return Response({'data': chapter_notes})
        if title:
            chapter_notes = ChapterNotes.objects.filter(chapter__title__icontains=title)
            print(chapter_notes.query)
           # return Response({'data': chapter_notes})
        for i in chapter_notes:
            resp = {}
            resp['chapter_id'] = i.chapter.id
            resp ['chapter_notes'] = i.file_url
            result.append(resp)
        print(result)
        return Response({'data': result})



class SubChapterView(APIView):
    
    def get(self, request):
        data = request.GET
        chap_id = str(data.get('chapter_id'))
        title = data.get('title')
        if chap_id.isdigit():
            sub_chap = Subchapters.objects.filter(chapter_id=chap_id).values()
            return Response({'data': sub_chap})
        if title:
            sub_chap = Subchapters.objects.filter(title__icontains=title).values()
            return Response({'data': sub_chap})
        return Response({'message': 'Chapter ID not provided'})


class TeachersView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        data = request.GET
        teacher_id = data.get('teacher_id')
        print(data)
        resp = []
        try:
            if 'teacher_id' in data:
                teacher = TeacherProfile.objects.get(id=teacher_id)
                teacher_dict = {'id': teacher.id, 'name': teacher.name, 'profile_pic': teacher.profile_pic.url if teacher.profile_pic else None}
                resp.append(teacher_dict)
                return Response({'data': resp})
            else:
                teacher = TeacherProfile.objects.filter().all()
                teacher_dict = {'id': teacher.id, 'name': teacher.name, 'profile_pic': teacher.profile_pic.url if teacher.profile_pic else None}
                resp.append(teacher_dict)
                return Response({'data': resp})
        except Exception as e:
            return Response({'message': 'We could not find anything', 'error': str(e)})


class TopicsView(APIView):
    def get(self, request):
        data = request.GET
        print(data)
        topic_id = data.get('topic_id')
        subchap_id = data.get('subchapter_id')
        chapter_id = data.get('chapter_id')
        subject_id = data.get('subject_id')
        res = []
        topics = None
        if data:
            if topic_id:
                topics = Topics.objects.filter(id=topic_id)
            if subchap_id:
                topics = Topics.objects.filter(subchapter__in=subchap_id)
            if chapter_id:
                topics = Topics.objects.filter(subchapter__chapter__in=chapter_id)
            if subject_id:
                topics = Topics.objects.filter(subchapter__chapter__subject__in=subject_id)
            if not topics:
                return Response({'message':"Could not find what you were searching for"})
        else:
            topics = Topics.objects.filter().all()
        for topic in topics:
            resp_dict = {
                'id': topic.id,
                'title':topic.title,
                'thumbnailUrl': topic.thumbnailUrl.url if topic.thumbnailUrl else None
                }
            res.append(resp_dict)
        return Response({'data': res})


class LiveClassesView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        data = request.GET
        resp = []
        teacher_id = data.get('teacher_id')
        live_id = data.get('live_id')
        if data:
            if teacher_id:
                classes = LiveClasses.objects.filter(teacher_profile__id=teacher_id)
            elif live_id:
                classes = LiveClasses.objects.filter(id=live_id)
            else:
                classes = LiveClasses.objects.filter().all()
        for i in classes:
            image_url = i.teacher_profile.profile_pic
            teacher = model_to_dict(i.teacher)
            resp_dict = model_to_dict(i)
            resp_dict['teacher'] = teacher
            resp_dict['thumbnail'] = resp_dict['thumbnail'].url if resp_dict['thumbnail'] else None
            resp.append(resp_dict)
        return Response({'data': resp})


class QuestionSetView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        data = request.data
        print(data)
        questions_obj = Questions(
            title = data.get('title'),
            topic_id = data.get('topic_id'),
            question_image_file = data.get('question_image_file'),
            hint = data.get('hint'),
            hint_image = data.get('hint_image'),
            solution = data.get('solution'),
            sol_image = data.get('sol_image'),
            difficulty_level = data.get('difficulty_level'),
            type_of_question = data.get('type_of_question'),
            source = data.get('source'),
            weightage = data.get('weightage'),
            is_practice_test = data.get('is_practice_test')
        )
        questions_obj.save()
        options = data.get('options')
        print(options, type(options))

        for i in options:
            options_obj = AnswerOptions(
                question = questions_obj,
                answer_options = i.get("text"),
                is_correct = i.get("is_correct", False)
            )
            options_obj.save()
        return Response({'message': 'Question is added successfully!'})

    def get(self, request):
        data = request.GET
        print(data)
        question_list = []
        question_res = []
        question_option_mapping = {}
        topic_id_list = json.loads(data.get('topic_id'))
        question_count = int(data.get('question_count'))
        is_practice_test = json.loads(data.get('is_practice_test', False))
        print(topic_id_list, type(topic_id_list))
        
        if topic_id_list:
            question_list = Questions.objects.filter(topic_id__in=topic_id_list, is_practice_test=is_practice_test)[:question_count]
            options_list = AnswerOptions.objects.filter(question__in=question_list)
            for option in options_list:
                if option.question_id not in question_option_mapping:
                    question_option_mapping[option.question_id] = [model_to_dict(option)]
                else:
                    question_option_mapping[option.question_id].append(model_to_dict(option))
            print(question_option_mapping)
            print(question_list)
            
            for question in question_list:
               temp = model_to_dict(question)
               print(temp)
               temp['question_image_file'] = question.question_image_file.url if question.question_image_file else None
               temp['hint_image'] = question.hint_image.url if question.hint_image else None
               temp['sol_image'] = question.sol_image.url if question.sol_image else None
               temp['options'] = question_option_mapping.get(question.id)  #to get options for the particular question
               question_res.append(temp)
        return Response({'data': question_res})

    


    
