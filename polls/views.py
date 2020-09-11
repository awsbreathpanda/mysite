from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from polls.models import Choice, Question
from django.http.response import Http404, HttpResponse
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
