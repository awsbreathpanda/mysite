from rest_framework import viewsets
from polls.models import Question, Choice
from api.serializers import QuestionSerializer, ChoiceSerializer


# Create your views here.
class QuestionViewSet(viewsets.ModelViewSet):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ChoiceViewSet(viewsets.ModelViewSet):

    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
