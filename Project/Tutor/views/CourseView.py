from django.utils.regex_helper import Choice
from django.views import generic
from django.shortcuts import render, redirect
from UserAuthentication.models import User
from Tutor.forms import AddCourseForm
from Tutor.models import TutorCourse
from Course.models import Course
from django.contrib import messages


def create_context(add_course_form):

    context = {
        'add_course_form': add_course_form,
    }
    return context


class CourseView(generic.View):
    template_name = 'Tutor/tutorCourse.html'
    user: User = None

    def get(self, request):
        
        user: User = User.objects.get(pk=request.user.id)
        if user.is_tutor():
            dic = {'user': user}
            add_course_form = AddCourseForm(**dic)
            return render(request, self.template_name, create_context(add_course_form))
        return redirect('index')

    def post(self, request):
        user: User = User.objects.get(pk=request.user.id)
        if user.is_tutor():
            choiceForm = AddCourseForm(request.POST or None)
            if choiceForm.is_valid():
                choice = choiceForm.cleaned_data['choices']
                if choice is not None and choice != '' :
                    course = Course.objects.get(course_name=choice)
                    tutor_course = TutorCourse(user=user, course=course)
                    tutor_course.save()
                    messages.add_message(request, messages.SUCCESS, 'Curso agregado exitosamente')
                    dic = {'user': user}
                    add_course_form = AddCourseForm(**dic)
                    return render(request, self.template_name, create_context(add_course_form))
                else:
                    messages.add_message(request, messages.ERROR, 'El curso no ha sido agregado')
                    dic = {'user': user}
                    add_course_form = AddCourseForm(**dic)
                    return render(request, self.template_name, create_context(add_course_form))

        return redirect('index')

