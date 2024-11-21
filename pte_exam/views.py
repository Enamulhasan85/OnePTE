from rest_framework import generics
from .models import Question
from .serializers import QuestionSerializer, QuestionDetailSerializer
from rest_framework.exceptions import NotFound
from rest_framework.response import Response


class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned questions to a given question type,
        by filtering against a `question_type` query parameter in the URL.
        """
        queryset = self.queryset
        question_type = self.request.query_params.get('question_type', None)
        if question_type is not None:
            queryset = queryset.filter(question_type=question_type)
        return queryset
    


class QuestionDetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionDetailSerializer

    def get_object(self):
        question_id = self.kwargs.get('pk')
        try:
            return Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise NotFound("Question not found")

