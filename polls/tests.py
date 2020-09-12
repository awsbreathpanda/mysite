from django.test import TestCase
from django.utils.timezone import now, timedelta
from .models import Question
from django.urls import reverse


# Create your tests here.
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = now() + timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = now() - timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = now() - timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)

        self.assertIs(recent_question.was_published_recently(), True)


class IndexViewTests(TestCase):
    def test_get_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_get_question(self):
        Question.objects.create(question_text='Demo question.')

        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Demo question.>'])
