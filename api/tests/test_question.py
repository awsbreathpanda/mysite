# DRF的测试，用绝对路径，不要使用reverse
from rest_framework.test import APITestCase
from polls.models import Question


class QuestionViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.question = Question.objects.create(question_text='hello world?')

    def test_get_list(self):
        url = '/api/questions/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_get_detail(self):
        url = '/api/questions/' + str(self.question.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        url = '/api/questions/'
        data = {'question_text': 'hello libin?'}
        response = self.client.post(
            url,
            data=data,
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        question = Question.objects.get(question_text=data['question_text'])
        self.assertIsNotNone(question)
