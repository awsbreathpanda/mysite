from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from polls.models import Choice, Question
from django.http.response import Http404
from django.views.generic.base import View

# Create your views here.


# polls/
class IndexView(View):
    def get(self, request):
        latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
        return render(request,
                      'polls/index.html',
                      context={
                          'latest_question_list': latest_question_list,
                      })


# polls/detail/(id)/
class DetailView(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            next_url = reverse(
                'polls:login') + '?next=' + request.get_full_path()
            return redirect(next_url)

        try:
            question = Question.objects.get(id=id)
        except Question.DoesNotExist:
            raise Http404('Question Does not exist')

        return render(request,
                      'polls/detail.html',
                      context={
                          'question': question,
                      })

    def post(self, request, id):
        choice_id = request.POST.get('choice')

        question = get_object_or_404(Question, id=id)
        try:
            selected_choice = question.choice_set.get(id=choice_id)
        except Choice.DoesNotExist:
            return render(request,
                          context={
                              'question': question,
                              'error_message': "You didn't select a choice"
                          })

        selected_choice.votes += 1
        selected_choice.save()

        # return redirect(reverse('polls:result', args=(question.id, )))
        return redirect(reverse('polls:result', args=(question.id, )))


# polls/vote/(id)/
class ResultView(View):
    def get(self, request, id):
        question = get_object_or_404(Question, id=id)
        return render(request,
                      'polls/result.html',
                      context={
                          'question': question,
                      })


# polls/register/
class RegisterView(View):
    def get(self, request):
        return render(request, 'polls/register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, password]):
            return redirect(reverse('polls:register'))

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user is not None:
            return redirect(reverse('polls:register'))

        user = User.objects.create_user(username=username, password=password)
        user.is_active = 1
        user.save()

        return redirect(reverse('polls:index'))


# polls/login/
class LoginView(View):
    def get(self, request):
        return render(request, 'polls/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, password]):
            return redirect('polls:login')

        print(username + ',' + password)
        user = authenticate(request, username=username, password=password)
        if user is None:
            return redirect('polls:login')

        if not user.is_active:
            return redirect('polls:login')

        login(request, user)

        next_url = request.GET.get('next', reverse('polls:index'))

        return redirect(next_url)


# polls/logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('polls:index'))
