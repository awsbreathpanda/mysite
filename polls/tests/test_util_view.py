from django.test import TestCase
from django.utils.timezone import now, timedelta
from polls.models import Choice, Question
from django.contrib.auth.models import User

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


class DetailViewTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='libin', password='123')
        self.question = Question.objects.create(
            question_text='unit_test question?')
        self.choice_good = Choice.objects.create(question=self.question,
                                                 choice_text='good',
                                                 votes=0)
        self.choice_soso = Choice.objects.create(question=self.question,
                                                 choice_text='soso',
                                                 votes=0)
        self.choice_bad = Choice.objects.create(question=self.question,
                                                choice_text='bad',
                                                votes=0)

    def tearDown(self) -> None:
        self.question.delete()
        self.user.delete()

    def test_get(self):

        self.client.login(username='libin', password='123')
        response = self.client.get(
            reverse('polls:detail', kwargs={'id': self.question.id}))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(str(response.context['question']),
                         self.question.question_text)

    def test_post(self):

        self.client.login(username='libin', password='123')
        response = self.client.post(reverse('polls:detail',
                                            kwargs={'id': self.question.id}),
                                    data={
                                        'choice': self.choice_good.id,
                                    })

        self.assertEqual(response.status_code, 302)

        good_choice_votes = Choice.objects.get(id=self.choice_good.id).votes
        self.assertEqual(good_choice_votes, 1)
